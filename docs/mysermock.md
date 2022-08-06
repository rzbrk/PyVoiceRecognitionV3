Help on module mysermock:

NAME
    mysermock

CLASSES
    builtins.object
        MySerMock
    
    class MySerMock(builtins.object)
     |  MySerMock(inbuffer=None, timeout=None)
     |  
     |  Mockup for serial device
     |  
     |  Methods defined here:
     |  
     |  __init__(self, inbuffer=None, timeout=None)
     |      Initialize instance
     |      
     |      Parameters:
     |          * inbuffer (bytearray): input buffer
     |          * timeout (int): read timeout in seconds
     |      
     |      Returns:
     |          Nothing
     |  
     |  append_to_inbuffer(self, data)
     |      Append new data to the input buffer
     |      
     |      Parameters:
     |          * data (bytearray): data to be append to the input buffer
     |      
     |      Returns:
     |          Nothing
     |  
     |  inWaiting(self)
     |      Returns the current size of the input buffer
     |      
     |      Parameters:
     |          Nothing
     |      
     |      Returns:
     |          * length (int): Length of input buffer in bytes
     |  
     |  read(self, n_bytes)
     |      Read data from mock serial port
     |      
     |      Parameters:
     |          * n_bytes (int): Number of bytes to read. If n_bytes is larger than
     |              the data in the input buffer than this method can return less
     |              data.
     |      
     |      Returns:
     |          * data (bytes)
     |  
     |  reset_input_buffer(self)
     |      Fakes resetting the input buffer
     |      
     |      This method actually does nothing and will not reset anything. For the
     |      purposes of testing this is expected.
     |  
     |  write(self, data)
     |      Write data to mock serial port
     |      
     |      This method actually does nothing
     |      
     |      Parameters:
     |          * data (bytearray): data to be sent
     |      
     |      Returns:
     |          Nothinng
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FILE
    /home/jan/Projekte/Programme/PyVoiceRecognitionV3/PyVoiceRecognitionV3/mysermock.py


