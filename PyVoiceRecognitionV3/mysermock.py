import time

class MySerMock:
    """
    Mockup for serial device
    """
    def __init__(self, inbuffer=None, timeout=None):
        """
        Initialize instance

        Parameters:
            * inbuffer (bytearray): input buffer
            * timeout (int): read timeout in seconds

        Returns:
            Nothing
        """

        # Initialize the input buffer inbuffer
        if None != inbuffer:
            self.inbuffer = inbuffer
        else:
            # Empty input buffer
            self.inbuffer = bytearray(b'')

        if None != timeout:
            self.timeout = timeout
        else:
            self.timeout = 60

        # Initialize the output buffer outbuffer. The output buffer can be used
        # to check what would have been sent to the module. The write() methods
        # appends to outbuffer.
        self.outbuffer =bytearray(b'')

    def read(self, n_bytes):
        """
        Read data from mock serial port

        Parameters:
            * n_bytes (int): Number of bytes to read. If n_bytes is larger than
                the data in the input buffer than this method can return less
                data.

        Returns:
            * data (bytes)
        """
        len_data = min(len(self.inbuffer), n_bytes)
        data = self.inbuffer[0:len_data]

        # Simulate timeout
        if n_bytes > len(self.inbuffer):
            time.sleep(self.timeout)

        # What is read is removed from inbuffer
        self.inbuffer = self.inbuffer[len_data:]

        return bytes(data)

    def inWaiting(self):
        """
        Returns the current size of the input buffer

        Parameters:
            Nothing

        Returns:
            * length (int): Length of input buffer in bytes
        """
        return len(self.inbuffer)

    def write(self, data):
        """
        Write data to mock serial port

        This method actually append data to outbuffer

        Parameters:
            * data (bytearray): data to be sent

        Returns:
            Nothinng
        """
        self.outbuffer.extend(data)

    def reset_input_buffer(self):
        """
        Fakes resetting the input buffer

        This method actually does nothing and will not reset anything. For the
        purposes of testing this is expected.
        """
        pass

    def append_to_inbuffer(self, data):
        """
        Append new data to the input buffer

        Parameters:
            * data (bytearray): data to be append to the input buffer

        Returns:
            Nothing
        """
        self.inbuffer.extend(data)

