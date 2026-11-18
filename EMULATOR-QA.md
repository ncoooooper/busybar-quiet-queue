# Firmware verification

BUSY Bar Emulator 0.1.0-beta.5, firmware 1.3.1.

Two visitors joined through the web form. Replaying each form returned its original number. The emulator showed ticket 1 and its topic. Click accepted ticket 1 and exposed ticket 2. Restarting the SQLite service retained ticket 2. Replaying acceptance of ticket 1 returned HTTP 409 without advancing. A final device click emptied the queue. The guest listener did not expose the operator queue.

The app was typechecked, built, installed and exercised on the emulator. Native captures are under screenshots/. The tested installable archive is in packages/.

Firmware motion pass: up, down, ok. 17 distinct frames in the controls recording. App io.ncoooooper.quietqueue exited: finished; heap peak 81.7 of 128 KiB.

## Display capture

Firmware 1.3.1 rendered both README examples. The display run replayed sample inputs in a separate emulator project. The source test above describes how those readings were obtained. Each square in a guide GIF is one front LED in a 16 × 16 cell. The production archive was built from the source in this repository.

## Screen transition capture

Firmware 1.3.1 rendered the display sequences in the README. The release archive also ran on a fresh emulator with rapid wheel reversals and Back during a transition. The guide uses a 14 × 14 lit area inside each 16 × 16 cell. Input sequences, frame counts and the release archive checksum are in [the capture record](media/screen-transitions.json).
