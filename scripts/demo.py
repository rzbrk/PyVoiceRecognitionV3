import PyVoiceRecognitionV3 as pvr3
from serial import Serial
dev=Serial(port="/dev/ttyUSB0", baudrate=9600)
vr=pvr3.PyVoiceRecognitionV3(device=dev)

