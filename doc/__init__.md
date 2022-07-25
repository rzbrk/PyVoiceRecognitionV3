Help on module __init__:

NAME
    __init__

CLASSES
    builtins.object
        PyVoiceRecognitionV3
    
    class PyVoiceRecognitionV3(builtins.object)
     |  PyVoiceRecognitionV3(port='/dev/ttyUSB0', baudrate=9600, tout=10, latency=50)
     |  
     |  Python class to interact with the Elechouse Voice Recognition Module V3
     |  
     |  Methods defined here:
     |  
     |  __init__(self, port='/dev/ttyUSB0', baudrate=9600, tout=10, latency=50)
     |      Create an instance of class ``PyVoiceRecognitionModuleV3``
     |      
     |      Returns an instance and immediately opens a serial port connection to
     |      the voice recognition module connected to the serial port ``port``.
     |      
     |      Parameters:
     |          port (device name): device name
     |          baudrate (int or None): baud rate such as 9600 or 2400. If None
     |              defaults to 9600 baud.
     |          tout (int): timeout for the serial communication in milliseconds
     |              (ms)
     |          latency (int): latency for the response from the module in
     |              milliseconds (ms)
     |      
     |      Returns:
     |          Nothing
     |  
     |  check_recognizer(self)
     |      Checks recognizer (01)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |                  "raw": response_bin,
     |                  "no_records_in_recognizer": rvn,
     |                  "records_in_recognizer": vri_dec,
     |                  "group_mode": grpm,
     |                  }
     |      
     |      Parameters:
     |          None
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |  
     |  check_record_train_status(self, record=None)
     |      Checks record train status (02)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |                  "raw": response_bin,
     |                  "no_trained_records": n,
     |                  "trained_records": rec,
     |                  "train_status": sta,
     |                  }
     |      Parameters:
     |          record (None or int): record number to be checked. If None,
     |              all records will be checked.
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |  
     |  check_system_settings(self)
     |      Checks system settings (00)
     |      
     |      The method returns a dictionary containing the response from the
     |      module:
     |      
     |          response_dict = {
     |                  "raw": response_bin,
     |                  "trained": sta,
     |                  "rec_value_out_of_range": rverr,
     |                  "baudrate": br,
     |                  "output_io_mode": iom,
     |                  "output_io_pulse_width_ms": iopw,
     |                  "autoload": al,
     |                  "group_control": grp,
     |                  }
     |      
     |      Parameters:
     |          None
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the module
     |  
     |  clear_recognizer(self)
     |      Clear recognizer and stop recognizing (31)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = { "status": sta }
     |      
     |      Parameters:
     |          None
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |  
     |  load_to_recognizer(self, *records)
     |      Load record(s) to recognizer (30)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |                  "raw": response_bin,
     |                  "no_records_in_recognizer": n,
     |                  "records_in_recognizer": rec,
     |                  "status": sta,
     |                  }
     |      
     |      Parameters:
     |          records (int): Record number(s) to be loaded
     |              to recognizer.
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |  
     |  record_recognized(self, timeout=None, callback_func=None)
     |      Wait until trained record is recognized (0d)
     |      
     |      This method requires that at least one record is loaded to the
     |      recognizer of the module. It waits until ``timeout`` for a response
     |      message indicating that the module recognized a voice input.
     |      
     |      A callback function can be defined by ``callback_func``. If no custom
     |      callback function is provided (``None``) the default callback function
     |      ``_default_callback`` is used.
     |      module. The dictionary for the response has the following keys:
     |      
     |      * raw (bytearray): raw message from module
     |      * time_passed_ms (float): time of recognition in miliseconds after invocation
     |        of method ``record_recognized()``
     |      * records_in_recognizer (array of int): list of records in recognizer
     |      * recognized_record (int): the record number of the recognized record
     |      * index_recognized_record (int): index of the recognized record in the
     |        recognizer
     |      * signature_recognized_record (str or None): signature of the recognized
     |        record if present, otherwise ``None``
     |      * group_mode (int or None): group mode of module
     |      
     |      A sample custom callback function could look like:
     |      
     |          def custom_callback_function(response):
     |              print("Recognized something!")
     |              for key, value in response.items():
     |                  print("  ", key, value)
     |              print("")
     |      
     |      Parameters:
     |          timeout (int): Timeout in milliseconds to wait for
     |              a recognition
     |          callback_func (Name of callback function or None): Name
     |              of callback function to call when record is recognized.
     |      
     |      Returns:
     |          Nothing
     |  
     |  send_cmd(self, command)
     |      Sending a command to the module and receiving response(s)
     |      
     |      Parameters:
     |          command (bytearray): command to be sent to the module
     |      
     |      Returns:
     |          messages (array of bytearray): response messages from
     |              the module
     |  
     |  train_record(self, record=None)
     |      Train a record (20)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |              "raw": response_bin,
     |              "record": record,
     |              "training_status": sta
     |                  }
     |      
     |      Parameters:
     |          record (int): Record number to train
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

DATA
    iopw_conv = (10, 15, 20, 25, 30, 35, 40, 45, 50, 75, 100, 100, 300, 40...

FILE
    /home/jan/Projekte/Programme/PyVoiceRecognitionV3/PyVoiceRecognitionV3/__init__.py


