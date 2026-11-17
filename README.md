# Quiet Queue

Give visitors a numbered web ticket and accept the next request from your BUSY Bar.

Guests join from a small web form. Ticket numbers appear on the front while the operator sees the optional topic on the back. Click accepts the displayed ticket, Start refreshes, and the wheel switches to waiting count. The queue refreshes every ten seconds.

## Set up the queue

Run `python3 bridge/queue_server.py` on a host with Python 3.9+. Open http://127.0.0.1:8767/ to join. Set the app’s Operator server URL to `http://127.0.0.1:8766` and allow port 8766 in the emulator. Guest and operator endpoints have separate listeners. Both default to loopback. To share the guest form on a trusted LAN use `--guest-host 0.0.0.0` and share the host address with visitors. A physical device requires an operator address reachable from the device. Limit access to its port to the operator device on your trusted network. The operator API uses no credentials.

SQLite keeps FIFO order through restarts. Repeating a join with the same form token returns the same ticket. Each accept checks the expected ticket ID. Topics are erased upon acceptance. Use a short ASCII topic without private information. The guest page has no access to the ticket list.

## Run locally

From this folder, run `~/.busy-emulator/bin/busy-emulator dev --once` with BUSY Bar Emulator open. Back exits.

![BUSY Bar front display](screenshots/front-1.png)
