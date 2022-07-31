# PyVoiceRecognitionV3

## Description
`PyVoiceRecognitionV3` is a Python class (driver) for the [Elechouse Voice
Recognition Module V3](https://www.elechouse.com/product/speak-recognition-voice-recognition-module-v3/). The class features configuring, training and monitoring the recognition of the module.

## Installation
```
git clone https://github.com/rzbrk/PyVoiceRecognitionV3.git
cd PyVoiceRecognitionV3/
python -m pip install --user -e .
```

## The Elechouse Voice Recognition Module V3.1

![Elechouse Voice Recognition Module V3.1](./assets/module_with_mic.jpg)

The Elechouse Voice Recognition module is a speaker-dependent voice recognition module. The V3.1 series of module can be trained up to 255 verbal commands (records) of 1500 ms each. 7 of these records can be simultaniously loaded to a recognizer. The module compares audio recorded by a connected microphone and tries to match it to one of the records in the recognizer. If there is a match it will provide a result. The communication of the module with the outside world is facilitated via 5V GPIO and/or UART ports. More information about the module can be found on the [manufacturer website](https://www.elechouse.com/product/speak-recognition-voice-recognition-module-v3/).

NOTE: The description and manual provided on the manufacturers website refer to
an older version of this module (V3). This module version could only store up
to 80 voice commands. This driver was tested with a module V3.1 but should also
work with a module V3.

### Signatures
For each trained record a signature can be stored on the module. A signature
can be considered as a text label up to 26 characters (for model V3.1) and can
be used to name a record as a way to distinguish records.

### Group Control
Group control can be used to load records into the recognizer. There exist
system and user groups.

#### System Groups
Each system group holds 7 records. The system groups are fixed groups:

| System Group # | Records in group |
<<<<<<< HEAD
|---|---|
=======
>>>>>>> 7ed96151b3c8013caf0326b614dbe1a178498dd8
| 0 | 0 - 6 |
| 1 | 7 - 13 |
| 2 | 14 - 20 |
| 3 | 21 - 27 |
| ... | ... |

A system group can be loaded to the recognizer.

#### User Groups
Each user group holds 7 records as for system groups. But user groups allow
flexible grouping of any 7 records. User groups can be defined or deleted by
commands. A user group can then be loaded to the recognizer.

### Images
![Elechouse Voice Recognition Module V3.1 - top side](./assets/module_top.jpg)

![Elechouse Voice Recognition Module V3.1 - bottom side](./assets/module_bottom.jpg)

## Source Code Documentation

See [here](docs/README.md).
