"""Private FIFO queue for BUSY Bar. Run with Python 3.9 or later."""
import argparse
import json
import secrets
import sqlite3
import threading
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

STYLE = """<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quiet Queue</title><style>
*{box-sizing:border-box}body{background:#f3f3ed;color:#142f2a;font:1.14rem/1.5 system-ui;margin:0}
main{max-width:32rem;margin:10vh auto;padding:2rem}h1{font-size:2.65rem;letter-spacing:-.06em;line-height:1}
button{background:#175342;color:white;border:0;border-radius:.4rem;width:100%;padding:.85rem;font:inherit}
input{width:100%;margin:.5rem 0 1rem;padding:.75rem;font:inherit}small{color:#50645e}a{color:#175342}
</style>"""
def make_handler(dbpath, operator):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, body, kind="application/json", location=None):
            raw = (json.dumps(body) if kind == "application/json" else body).encode()
            self.send_response(status)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'")
            if location:
                self.send_header("Location", location)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def page(self, title, body):
            self.reply(200, STYLE + "<main><h1>" + title + "</h1>" + body + "</main>", "text/html")

        def do_GET(self):
            target = urlsplit(self.path)
            if operator and target.path == "/queue":
                with closing(sqlite3.connect(dbpath)) as db:
                    row = db.execute("SELECT (SELECT count(*) FROM tickets WHERE done=0), id, topic "
                                     "FROM tickets WHERE done=0 ORDER BY id LIMIT 1").fetchone()
                count, head, topic = row or (0, 0, "")
                return self.reply(200, {"count": count, "head": head, "topic": topic})
            if not operator and target.path == "/":
                token = secrets.token_hex(16)
                return self.page("Quiet Queue", "<p>Request a turn at this desk. Your host will call your ticket number.</p>"
                    '<form method="post" action="/join"><label>Topic <small>(optional, 24 characters)</small>'
                    '<input name="topic" maxlength="24" pattern="[ -~]*" autocomplete="off"></label>'
                    '<input type="hidden" name="nonce" value="' + token + '"><button>Join the queue</button></form>')
            if not operator and target.path == "/ticket":
                ticket = parse_qs(target.query).get("id", [""])[0]
                if ticket.isascii() and ticket.isdigit() and len(ticket) <= 12:
                    return self.page("Ticket #" + ticket, "<p>Listen for your number. You can close this page.</p>")
            self.reply(404, {"error": "Unknown route"})

        def do_POST(self):
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 2048:
                    return self.reply(400, {"error": "Invalid request length"})
                data = self.rfile.read(size).decode("utf-8")
                if operator and self.path == "/accept" and self.headers.get_content_type() == "application/json":
                    head = json.loads(data)["head"]
                    if type(head) is not int or head <= 0:
                        raise ValueError()
                    with closing(sqlite3.connect(dbpath)) as db, db:
                        cur = db.execute("UPDATE tickets SET done=1, topic='' WHERE id=? AND id=(SELECT min(id) FROM tickets WHERE done=0)", (head,))
                        changed = cur.rowcount == 1
                    return self.reply(200 if changed else 409, {"accepted": changed})
                if not operator and self.path == "/join" and self.headers.get_content_type() == "application/x-www-form-urlencoded":
                    fields = parse_qs(data, max_num_fields=3)
                    topic = fields.get("topic", [""])[0].strip()
                    nonce = fields["nonce"][0]
                    if len(nonce) != 32 or any(c not in "0123456789abcdef" for c in nonce):
                        raise ValueError()
                    if len(topic) > 24 or any(not 32 <= ord(c) <= 126 for c in topic):
                        return self.reply(400, {"error":"Use up to 24 printable ASCII characters."})
                    with closing(sqlite3.connect(dbpath)) as db, db:
                        db.execute("BEGIN IMMEDIATE")
                        existing = db.execute("SELECT id FROM tickets WHERE nonce=?", (nonce,)).fetchone()
                        if existing:
                            ticket = existing[0]
                        else:
                            if db.execute("SELECT count(*) FROM tickets WHERE done=0").fetchone()[0] >= 100:
                                return self.reply(429, {"error":"Queue full. Try again later."})
                            ticket = db.execute("INSERT INTO tickets(nonce,topic) VALUES(?,?)", (nonce,topic)).lastrowid
                    return self.reply(303, "", "text/plain", "/ticket?id=" + str(ticket))
                self.reply(404, {"error":"Unknown route"})
            except (KeyError, IndexError, TypeError, UnicodeError, ValueError, OverflowError):
                self.reply(400, {"error":"Invalid request"})
            except sqlite3.Error:
                self.reply(503, {"error":"Queue temporarily unavailable"})

    return Handler

def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--database", default="quiet-queue.sqlite3")
    args.add_argument("--operator-host", default="127.0.0.1")
    args.add_argument("--guest-host", default="127.0.0.1")
    args.add_argument("--operator-port", type=int, default=8766)
    args.add_argument("--guest-port", type=int, default=8767)
    config = args.parse_args()
    with closing(sqlite3.connect(config.database)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY, nonce TEXT UNIQUE NOT NULL, topic TEXT NOT NULL, done INTEGER DEFAULT 0)")
    with ThreadingHTTPServer((config.operator_host, config.operator_port), make_handler(config.database, True)) as ops, \
         ThreadingHTTPServer((config.guest_host, config.guest_port), make_handler(config.database, False)) as guests:
        threading.Thread(target=guests.serve_forever, daemon=True).start()
        try:
            ops.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
