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

class Test_reset_output_io(unittest.TestCase):
    """
    Tests for method reset_output_io()
    """

    def test_args_none(self):
        """
        reset_output_io(): No argument
        """
        exp_mod_cmd = bytearray(b'\xaa\x09\x14\x00\x01\x02\x03\x04\x05\x06\x0a')
        mod_rsp = bytearray(b'\xaa\x03\x14\x00\x0a')
        mockdev.reset()
        mockdev.append_to_inbuffer(mod_rsp)
        exp_rsp = {
            "raw": [mod_rsp],
            "output_io_resetted": list(range(7)),
                }

        rsp = vr.reset_output_io()

        # Check command sent to module
        self.assertEqual(mockdev.outbuffer, exp_mod_cmd)
        # Check return value from method
        self.assertEqual(rsp, exp_rsp)

    def test_args_all_pins_ordered(self):
        """
        reset_output_io(): All pins in method's argument (ordered)
        """
        exp_mod_cmd = bytearray(b'\xaa\x09\x14\x00\x01\x02\x03\x04\x05\x06\x0a')
        mod_rsp = bytearray(b'\xaa\x03\x14\x00\x0a')
        mockdev.reset()
        mockdev.append_to_inbuffer(mod_rsp)
        exp_rsp = {
            "raw": [mod_rsp],
            "output_io_resetted": list(range(7)),
                }

        rsp = vr.reset_output_io(0,1,2,3,4,5,6)

        # Check command sent to module
        self.assertEqual(mockdev.outbuffer, exp_mod_cmd)
        # Check return value from method
        self.assertEqual(rsp, exp_rsp)

    def test_args_all_pins_unordered(self):
        """
        reset_output_io(): All pins in method's argument (unordered)
        """
        # Swaped order: 2 <--> 1
        exp_mod_cmd = bytearray(b'\xaa\x09\x14\x00\x02\x01\x03\x04\x05\x06\x0a')
        mod_rsp = bytearray(b'\xaa\x03\x14\x00\x0a')
        mockdev.reset()
        mockdev.append_to_inbuffer(mod_rsp)
        exp_rsp = {
            "raw": [mod_rsp],
            # In the following key value the pins are ALWAYS ordered
            "output_io_resetted": list(range(7)),
                }

        # Swaped order: 2 <--> 1
        rsp = vr.reset_output_io(0,2,1,3,4,5,6)

        # Check command sent to module
        self.assertEqual(mockdev.outbuffer, exp_mod_cmd)
        # Check return value from method
        self.assertEqual(rsp, exp_rsp)

    def test_args_selected_pins(self):
        """
        reset_output_io(): Reset selected pins, not all
        """
        # Reset only pins 0, 2, 1 (unordered)
        exp_mod_cmd = bytearray(b'\xaa\x05\x14\x00\x02\x01\x0a')
        mod_rsp = bytearray(b'\xaa\x03\x14\x00\x0a')
        mockdev.reset()
        mockdev.append_to_inbuffer(mod_rsp)
        exp_rsp = {
            "raw": [mod_rsp],
            # In the following key value the pins are ALWAYS ordered
            "output_io_resetted": list(range(3)),
                }

        rsp = vr.reset_output_io(0,2,1)

        # Check command sent to module
        self.assertEqual(mockdev.outbuffer, exp_mod_cmd)
        # Check return value from method
        self.assertEqual(rsp, exp_rsp)

    def test_args_selected_pins_doubled(self):
        """
        reset_output_io(): Reset selected pins, with one pin specified doubled
        """
        # Reset pins 1, 0, 2, 1 (unordered and pin 1 doubled)
        exp_mod_cmd = bytearray(b'\xaa\x06\x14\x01\x00\x02\x01\x0a')
        mod_rsp = bytearray(b'\xaa\x03\x14\x00\x0a')
        mockdev.reset()
        mockdev.append_to_inbuffer(mod_rsp)
        exp_rsp = {
            "raw": [mod_rsp],
            # In the following key value the pins are ALWAYS ordered
            "output_io_resetted": [0,1,1,2],
                }

        rsp = vr.reset_output_io(1,0,2,1)

        # Check command sent to module
        self.assertEqual(mockdev.outbuffer, exp_mod_cmd)
        # Check return value from method
        self.assertEqual(rsp, exp_rsp)

if __name__ == '__main__':
    unittest.main()
