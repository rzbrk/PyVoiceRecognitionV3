import sys
import unittest
from .MySerMock import MySerMock

sys.path.append('../.')
from PyVoiceRecognitionV3 import PyVoiceRecognitionV3

# Mockup for serial device
mockdev = MySerMock()

# Create instance of PyVoiceRecognitionV3
vr = PyVoiceRecognitionV3(device = mockdev)

class Test_init(unittest.TestCase):
    """
    Tests for method __init__
    """

    def test_isinstance(self):
        """
        Test if correct instance is returned
        """
        print("Test if correct instance is returned")
        self.assertIsInstance(
                PyVoiceRecognitionV3(device=mockdev),
                PyVoiceRecognitionV3
                )

class Test_send_cmd(unittest.TestCase):
    """
    Tests for method send_cmd()
    """

    def test_send_recv(self):
        """
        Test basic communication with method send_cmd()
        """
        print("Test basic communication with method send_cmd()")
        cmd = b'\xaa\x02\x00\x0a'    # check sys settings (00)
        exp_rsp = [bytearray(b'\xaa\x08\x00\x00\x00\x00\x00\x00\x00\x0a')]
        for msg in exp_rsp:
            mockdev.append_to_inbuffer(msg)

        rsp = vr.send_cmd(cmd)

        self.assertEqual(rsp,exp_rsp)

if __name__ == '__main__':
    unittest.main()
