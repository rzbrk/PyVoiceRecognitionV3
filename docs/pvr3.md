Help on module pvr3:

NAME
    pvr3

CLASSES
    builtins.Exception(builtins.BaseException)
        BadBaudrate
        BadMode
        BadSignature
    builtins.object
        PyVoiceRecognitionV3
    
    class BadBaudrate(builtins.Exception)
     |  Raised when baudrate is not supported by module.
     |  
     |  Method resolution order:
     |      BadBaudrate
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.Exception:
     |  
     |  __init__(self, /, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  __str__(self, /)
     |      Return str(self).
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args
    
    class BadMode(builtins.Exception)
     |  Raised when output IO mode is not supported by module.
     |  
     |  Method resolution order:
     |      BadMode
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.Exception:
     |  
     |  __init__(self, /, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  __str__(self, /)
     |      Return str(self).
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args
    
    class BadSignature(builtins.Exception)
     |  Raised when record signature contains bad characters (not in ASCII range 33
     |  to 126) or when record signature is too long (longer than 26 characters).
     |  
     |  Method resolution order:
     |      BadSignature
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.Exception:
     |  
     |  __init__(self, /, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  __str__(self, /)
     |      Return str(self).
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args
    
    class PyVoiceRecognitionV3(builtins.object)
     |  PyVoiceRecognitionV3(device=None, tout=10, latency=50)
     |  
     |  Python class to interact with the Elechouse Voice Recognition Module V3
     |  
     |  Methods defined here:
     |  
     |  __init__(self, device=None, tout=10, latency=50)
     |      Create an instance of class ``PyVoiceRecognitionModuleV3``
     |      
     |      Returns an instance and immediately opens a serial port connection to
     |      the voice recognition module connected to the serial device
     |      ``device``.
     |      
     |      Parameters:
     |          device (device): serial device
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
     |  check_record_signature(self, record=None)
     |      Check the signature of a record (03)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |              "raw": response_bin,
     |              "record": record,
     |              "signature": signature,
     |                  }
     |      
     |      The signature for a record (optional) can be considered as a "label"
     |      for the record. In principle, the module allows any ASCII character
     |      with ASCII code < 255. The maximum number of characters for the
     |      signature is 26 (derived from test on module V3.1). To avoid any
     |      potential problems the character range is limited from "!" (ASCII 33)
     |      to "~" (ASCII 126).
     |      
     |      Parameters:
     |          record (int): Record number
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
     |  restore_system_settings(self)
     |      Restore the system settings of the module to defaults (10)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |              "raw": response_bin,
     |                  }
     |      
     |      Parameters:
     |          None
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
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
     |  set_baudrate(self, baudrate=None)
     |      Set the baud rate of the module (11)
     |      
     |      The following baud rates are supported by the module:
     |      
     |      * 2400 baud
     |      * 4800 baud
     |      * 9600 baud
     |      * 19200 baud
     |      * 38400 baud
     |      
     |      The change of baudrate takes effect only after restarting the module.
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |              "raw": response_bin,
     |                  }
     |      
     |      Parameters:
     |          baudrate (int): baud rate
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |      
     |      Raises:
     |          BadBaudrate: When no or an unsupported baud rate is given
     |  
     |  set_output_io_mode(self, mode=None)
     |      Set the output IO mode (12)
     |      
     |      The output IO mode determines how the output pins of the module (OUT0
     |      ... OUT6) behave in case the module recognizes a voice command. The
     |      output pins represent the 7 records in the recognizer. For example, if
     |      the third record in the recognizer is recognized only OUT2 will be
     |      affected. There are 4 different modes:
     |      
     |      0 -- Pulse: Send negative pulse to output. The pulse width can be
     |           configured with the method set_output_io_pulse_width().
     |      1 -- Toggle: Toggle the output state each time a recognition takes
     |           place.
     |      2 -- Set: Set output to high when the module recognizes a voice
     |           command. The ouput state will stay high until the state is
     |           resetted with the method reset_output_io().
     |      2 -- Clear: Set output to low when the module recognizes a voice
     |           command. The ouput state will stay low until the state is
     |           resetted with the method reset_output_io().
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |              "raw": response_bin,
     |              "mode": output io mode,
     |                  }
     |      
     |      Parameters:
     |          mode (str): Output IO mode ("pulse", "toggle", "set", "clear")
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |      
     |      Raises:
     |          BadMode: When no or an unsupported output IO mode is given
     |  
     |  set_signature(self, record=None, signature=None)
     |      Set signature for record (22)
     |      
     |      The signature for a record (optional) can be considered as a "label"
     |      for the record. In principle, the module allows any ASCII character
     |      with ASCII code < 255. The maximum number of characters for the
     |      signature is 26 (derived from test on module V3.1). To avoid any
     |      potential problems the character range is limited from "!" (ASCII 33)
     |      to "~" (ASCII 126).
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |              "raw": response_bin,
     |              "record": record,
     |              "signature": signature,
     |                  }
     |      
     |      Parameters:
     |          record (int): Record number to train
     |          signature (str or None): Signature for record
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |      
     |      Raises:
     |          BadSignature: signature is too long or contains bad characters
     |  
     |  train_record(self, record=None, signature=None)
     |      Train a record without (20) or with signature (21)
     |      
     |      The method returns a dictionary containing the response message from
     |      the module:
     |      
     |          response_dict = {
     |              "raw": response_bin,
     |              "record": record,
     |              "signature": signature,
     |              "training_status": sta
     |                  }
     |      
     |      The signature for a record (optional) can be considered as a "label"
     |      for the record. In principle, the module allows any ASCII character
     |      with ASCII code < 255. The maximum number of characters for the
     |      signature is 26 (derived from test on module V3.1). To avoid any
     |      potential problems the character range is limited from "!" (ASCII 33)
     |      to "~" (ASCII 126).
     |      
     |      Parameters:
     |          record (int): Record number to train
     |          signature (str or None): Signature for record
     |      
     |      Returns:
     |          response (dict): dictionary containing the response
     |              from the voice recognition module
     |      
     |      Raises:
     |          BadSignature: signature is too long or contains bad characters
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
    br_conv = (9600, 2400, 4800, 9600, 19200, 38400)
    iomode_conv = ('pulse', 'toggle', 'set', 'clear')
    iopw_conv = (10, 15, 20, 25, 30, 35, 40, 45, 50, 75, 100, 100, 300, 40...
    sign_char_max_ascii = 126
    sign_char_min_ascii = 33
    sign_max_len = 26

FILE
    /home/jan/Projekte/Programme/PyVoiceRecognitionV3/PyVoiceRecognitionV3/pvr3.py


