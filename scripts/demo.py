from PyVoiceRecognitionV3 import PyVoiceRecognitionV3
from serial import Serial
dev=Serial(port="/dev/ttyUSB0", baudrate=9600)
vr=PyVoiceRecognitionV3(device=dev)

