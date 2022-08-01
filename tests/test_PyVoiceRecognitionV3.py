import sys
import unittest
from mock_serial import MockSerial

sys.path.append('../.')
import PyVoiceRecognitionV3 as pvr3

# Mockup for serial device
mockdev = MockSerial()
#mockdev.open()

# Create instance of PyVoiceRecognitionV3
vr = pvr3.PyVoiceRecognitionV3(device = mockdev)

class Test_init(unittest.TestCase):
    """
    Tests for method __init__
    """

    def test_isinstance(self):
        """
        Test if correct instance is returned
        """
        self.assertIsInstance(
                pvr3.PyVoiceRecognitionV3(device=mockdev),
                pvr3.PyVoiceRecognitionV3
                )

class Test_send_cmd(unittest.TestCase):
    """
    Tests for method send_cmd()
    """

    def test_send_recv(self):
        """

        """
        cmd = b'\xaa\x02\x00\x0a'    # check sys settings (00)
        rsp = b'\xaa\x08\x00\x00\x00\x00\x00\x00\x0a'

        mockdev.stub(
                receive_bytes = cmd,
                send_bytes = rsp,
                )

        r = vr.send_cmd(cmd)
        print(r)

        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
