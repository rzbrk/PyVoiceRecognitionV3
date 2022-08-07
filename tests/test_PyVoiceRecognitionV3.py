import sys
import unittest

sys.path.append('../.')
from PyVoiceRecognitionV3 import PyVoiceRecognitionV3, MySerMock
from PyVoiceRecognitionV3 import BadPulseWidth

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
        __init__(): Test if correct instance is returned
        """
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
        send_cmd(): Test basic communication
        """
        cmd = b'\xaa\x02\x00\x0a'    # check sys settings (00)
        exp_rsp = [bytearray(b'\xaa\x08\x00\x00\x00\x00\x00\x00\x00\x0a')]
        for msg in exp_rsp:
            mockdev.append_to_inbuffer(msg)

        rsp = vr.send_cmd(cmd)

        self.assertEqual(rsp,exp_rsp)

class Test_set_output_io_pulse_width(unittest.TestCase):
    """
    Tests for method set_output_io_pulsewidth()
    """

    def test_no_argument(self):
        """
        set_output_io_pulse_width(): No argument
        """
        self.assertRaises(BadPulseWidth, vr.set_output_io_pulse_width, None)

    def test_bad_pulsewidth(self):
        """
        set_output_io_pulse_width(): Bad argument/pulsewidth
        """
        # 42 ms in not a valid value for the pulse width
        self.assertRaises(BadPulseWidth, vr.set_output_io_pulse_width, 42)

    def test_valid_pulsewidth(self):
        """
        set_output_io_pulse_width(): Valid argument/pulsewidth
        """
        pw = 20 # milliseconds
        pw_hex = hex(2) # corresponding hex value
        mod_rsp = bytearray(b'\xaa\x03\x13\x00\x0a')
        mockdev.append_to_inbuffer(mod_rsp)
        exp_rsp = {
            "raw": [mod_rsp],
            "output_io_pulse_width_hex": pw_hex,
            "output_io_pulse_width_ms": pw,
                }
        rsp = vr.set_output_io_pulse_width(pulsewidth = pw)
        self.assertEqual(rsp, exp_rsp)

if __name__ == '__main__':
    unittest.main()
