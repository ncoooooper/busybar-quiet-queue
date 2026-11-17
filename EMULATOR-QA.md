# Firmware verification

BUSY Bar Emulator 0.1.0-beta.5, firmware 1.3.1.

Two visitors joined through the web form. Replaying each form returned its original number. The emulator showed ticket 1 and its topic. Click accepted ticket 1 and exposed ticket 2. Restarting the SQLite service retained ticket 2. Replaying acceptance of ticket 1 returned HTTP 409 without advancing. A final device click emptied the queue. The guest listener did not expose the operator queue.

The app was typechecked, built, installed and exercised on the emulator. Native captures are under screenshots/. The tested installable archive is in packages/.
