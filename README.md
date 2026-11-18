# Quiet Queue

Give visitors a numbered web ticket and accept the next request from your BUSY Bar.

The visitor needs only a web form and a number. At the desk, you can call that number from the front display and read the visitor’s topic on the operator side.

## Take a place in line

1. Open the guest form, enter a short optional topic and submit. Note the ticket number it returns. A guest who resubmits the same form gets the original ticket.
2. Check the bar for the ticket at the head of the queue. Turn the wheel to see how many visitors are waiting.
3. Turn back when you are ready to call someone. The clip shows ticket 1 at the front of a two-person queue.

![Ticket 1 gives way to the count of two waiting visitors.](media/guide/check-the-line.gif)

## Call the next visitor

1. Read the topic on the rear and call the displayed ticket number. Click the wheel to accept it.
2. The next ticket moves to the front. In this recording, ticket 2 follows ticket 1. When the last visitor is called, the front reads **All clear**.
3. Press **Start** to check the server immediately. The bar also checks on its own every ten seconds.

![Ticket 1 is accepted and the front display changes to Ticket 2.](media/guide/accept-next-ticket.gif)

## Set up the source

Guests join from a small web form. Ticket numbers appear on the front while the operator sees the optional topic on the back. Click accepts the displayed ticket, Start refreshes, and the wheel switches to waiting count. The queue refreshes every ten seconds.

## Set up the queue

Run `python3 bridge/queue_server.py` on a host with Python 3.9+. Open http://127.0.0.1:8767/ to join. Set the app’s Operator server URL to `http://127.0.0.1:8766` and allow port 8766 in the emulator. Guest and operator endpoints have separate listeners. Both default to loopback. To share the guest form on a trusted LAN use `--guest-host 0.0.0.0` and share the host address with visitors. A physical device requires an operator address reachable from the device. Limit access to its port to the operator device on your trusted network. The operator API uses no credentials.

SQLite keeps FIFO order through restarts. Repeating a join with the same form token returns the same ticket. Each accept checks the expected ticket ID. Topics are erased upon acceptance. Use a short ASCII topic without private information. The guest page has no access to the ticket list.

## Run in the emulator

Open BUSY Bar Emulator. From this repository, run:

```sh
~/.busy-emulator/bin/busy-emulator dev --once
```

Press **Back** to exit.

The GIFs are excerpts from the emulator recording. Each front-display pixel is shown at 9× its original width and height. The end frames pause for reading.

[Full recording](media/controls.mp4) · [Rear display](screenshots/back-1.png) · [Firmware test](EMULATOR-QA.md) · [MIT license](LICENSE)
