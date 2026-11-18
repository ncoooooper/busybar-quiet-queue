# Firmware verification

BUSY Bar Emulator 0.1.0-beta.5, firmware 1.3.1.

Two visitors joined through the web form. Replaying each form returned its original number. The emulator showed ticket 1 and its topic. Click accepted ticket 1 and exposed ticket 2. Restarting the SQLite service retained ticket 2. Replaying acceptance of ticket 1 returned HTTP 409 without advancing. A final device click emptied the queue. The guest listener did not expose the operator queue.

The app was typechecked, built, installed and exercised on the emulator. Native captures are under screenshots/. The tested installable archive is in packages/.

Firmware motion pass: up, down, ok. 17 distinct frames in the controls recording. App io.ncoooooper.quietqueue exited: finished; heap peak 81.7 of 128 KiB.

## Display capture

Firmware 1.3.1 rendered both README examples. The display run replayed sample inputs in a separate emulator project. The source test above describes how those readings were obtained. Each square in a guide GIF is one front-display pixel enlarged to 9 × 9. The production archive was built from the source in this repository.
