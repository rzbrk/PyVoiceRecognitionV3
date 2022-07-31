# PyVoiceRecognitionV3

## Installation
```
git clone https://github.com/rzbrk/PyVoiceRecognitionV3.git
cd PyVoiceRecognitionV3/
python -m pip install --user -e .
```

## Description
`PyVoiceRecognitionV3` is a Python class (driver) for the [Elechouse Voice
Recognition Module V3](https://www.elechouse.com/product/speak-recognition-voice-recognition-module-v3/). The class features configuring, training and monitoring the recognition of the module.

## The Elechouse Voice Recognition Module V3

![Elechouse Voice Recognition Module V3.1](./assets/module_with_mic.jpg)

The Elechouse Voice Recognition module is a speaker-dependent voice recognition module. The V3 series of module can be trained up to 80 verbal commands (records) of 1500 ms each. 7 of these records can be simultaniously loaded to a recognizer. The module compares audio recorded by a connected microphone and tries to match it to one of the records in the recognizer. If there is a match it will provide a result. The communication of the module with the outside world is facilitated via 5V GPIO and/or UART ports. More information about the module can be found on the [manufacturer website](https://www.elechouse.com/product/speak-recognition-voice-recognition-module-v3/).

![Elechouse Voice Recognition Module V3.1 - top side](./assets/module_top.jpg)

![Elechouse Voice Recognition Module V3.1 - bottom side](./assets/module_bottom.jpg)

## Source Code Documentation

See [here](docs/README.md).
