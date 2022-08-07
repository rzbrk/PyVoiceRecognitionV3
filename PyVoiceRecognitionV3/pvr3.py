import time

# Elechouse Voice Recognition Module V3*
# Protocol definition see:
# https://github.com/elechouse/VoiceRecognitionV3#protocol

# List to convert hex value for IO pulse width to milliseconds
iopw_conv = (10, 15, 20, 25, 30, 35, 40, 45, 50, 75, 100,
        100, 300, 400, 500, 1000)

# List to convert hex values for baudrate values
br_conv = (9600, 2400, 4800, 9600, 19200, 38400)

# List to convert hex values for output IO mode
iomode_conv = ("pulse", "toggle", "set", "clear")

# Properties for record signature
sign_max_len = 26               # Maximum length for signature
sign_char_min_ascii = 33        # Minimum ASCII code for sign. character
sign_char_max_ascii = 126       # Maximum ASCII code for sign. character

class BadSignature(Exception):
    """
    Raised when record signature contains bad characters (not in ASCII range 33
    to 126) or when record signature is too long (longer than 26 characters).
    """
    pass

class BadBaudrate(Exception):
    """
    Raised when baudrate is not supported by module.
    """
    pass

class BadMode(Exception):
    """
    Raised when output IO mode is not supported by module.
    """
    pass

class BadPulseWidth(Exception):
    """
    Raised when output IO pulsewidth is not supported by module.
    """
    pass

class BadIOPin(Exception):
    """
    Raised when output IO pin is not supported by module.
    """
    pass

class PyVoiceRecognitionV3:
    """
    Python class to interact with the Elechouse Voice Recognition Module V3
    """
    def __init__(self,
            device=None,                # Serial device
        # Even for the lowest baudrate possible (2400 baud)
        # transmitting one byte should not take longer than
        # 10 ms. If after this time we get no more byte than
        # assume all bytes of a response are transmitted.
            tout=10,                    # Timeout in ms
        # Especially after sending recognizer commands it
        # takes some time for the module to respond. A value
        # from experience is 50 ms. After this time we can
        # expect to get no response.
            latency=50,                 # Response latency in ms
            ):
        """
        Create an instance of class ``PyVoiceRecognitionModuleV3``

        Returns an instance and immediately opens a serial port connection to
        the voice recognition module connected to the serial device
        ``device``.

        Parameters:
            device (device): serial device
            tout (int): timeout for the serial communication in milliseconds
                (ms)
            latency (int): latency for the response from the module in
                milliseconds (ms)

        Returns:
            Nothing
        """

        self.ser = device
        self.latency = latency
        self.tout = tout

#        self.ser = serial.Serial(
#            port=self.port,
#            baudrate=self.baudrate,
#            parity=serial.PARITY_NONE,
#            stopbits=serial.STOPBITS_ONE,
#            bytesize=serial.EIGHTBITS
#        )

    def _compile_cmd(self, payload):
        """
        Compiles a command for the voice recognition module

        The module accepts defined commands following a protocol described in
        https://github.com/elechouse/VoiceRecognitionV3#protocol. The method
        accepts the command payload and returns the compliant command.

        Each command ist structured as following:

        |\xaa|[len]|[payload]|\x0a|

        ``[len]`` is computed by the length in bytes of ``[len]`` itself
        (always 1) plus the length of ``[payload]``.

        Parameters:
            payload (bytearray): payload to be sent to the module


        Returns:
            command (bytearray): compliant command following the menufacturer's
            protocol specifications
        """

        payload_len = len(payload)
        command = bytearray()

        if b'\x0a' == payload:
            pass
        else:
            command += b'\xaa'
            command += bytes([1 + payload_len])
            command += payload
            command += b'\x0a'

        return command

    def _send_cmd(self, command):
        """
        Sends command to the module

        Before sending a comand to the module the input buffer from the serial
        port will be flushed. This ensures that any response from the module
        read-in after sending to the module relates to the last command.

        Parameters:
            command (bytearray): command to be send to the module.

        Returns:
            Nothing
        """
        # Before sending a new command clear the input buffer
        self.ser.reset_input_buffer()
        self.ser.write(command)

    def _recv_rsp(self, tout=None, latency=None):
        """
        Receive response/data from the module

        The response messages follow a similar format/protocol as the commands.
        The response can be split up into individual messages.

        Each response is structured as following:

        |\xaa|[len]|[data]|\x0a|

        ``[len]`` is computed by the length in bytes of ``[len]`` itself
        (always 1) plus the length of ``[data]``.

        Parameters:
            tout (int or None): timeout of the serial communication in
                milliseconds (ms). If ``None`` defaults to ``self.tout``.
            latency (int): latency for the response from the module in
                milliseconds (ms). If ``None`` defaults to ``self.latency``.

        Returns:
            messages (array of bytearray): the response messages (one or
                multiple) from the module
        """

        if None == tout:        # Timeout in ms
            tout = self.tout
        if None == latency:     # Latency in ms
            latency = self.latency

        # Initialize array for byte stream from module
        response = bytearray()

        # For the first byte of the response allow a specific
        # latency
        last = time.time()
        while ((time.time() - last) < latency/1000.):
            if self.ser.inWaiting():
                response += self.ser.read(1)
                break   # Exit while loop

        # Read rest of response byte by byte until timeout
        # (tout) is reached
        last = time.time()
        while ((time.time() - last) < tout/1000.):
            if self.ser.inWaiting():
                response += self.ser.read(1)
                last = time.time()

        # The response from the voice recognition module consists
        # of one or multiple messages following a specific format.
        # A message begins with a frame head (\xaa) followed by a
        # specific number of data fields and finally a frame end
        # (\x0a or \n). The first data field after the frame head
        # denotes the number of data fields between the frame head
        # and the frame end.

        # Initialize array for response (messages) that can consist
        # of one or more messages.
        messages=[]

        # If response from the module is already less than 3 bytes
        # we can absolutely have no valid message at all. In this
        # case we do not need to go through the following while
        # loop.
        if len(response) >= 3:
            end_of_resp = False
        else:
            end_of_resp = True

        p = 0   # Position of "pointer" in response
        while not end_of_resp:
            # If necessary move p to the first occurance of the
            # frame head (\xaa or 170 (decimal))
            while response[p] != 170:
                # Move the pointer to the field containing the
                # number of data field (field after frame head)
                p += 1
                # The minimum-length message has 3 bytes:
                # \xaa\x01\x0a
                if not p < len(response) - 3:
                    end_of_resp = True
                    break

            # If a valid message starts at current position p then
            # at position (p+1) should be the length of the message
            # (l) without header field (\xaa) and end field (\x0a).
            # Therefore, at position (p+l+1) we expect the end
            # field (\x0a or 10 decimal). If this is the case,
            # extract this part as a message and set the pointer
            # to position (p+l+2).
            l = response[p+1]
            if p + l + 1 < len(response) and 10 == response[p+l+1]:
                # We can extract the message (incl. head + end field)
                messages.append(response[p:p+l+2])
                # Place pointer at start of expected next message
                p = p + l + 2
                # Check if we already reached end of response
                if not p < len(response):
                    end_of_resp = True
            else:
                # Try again by restarting at next byte
                p += 1

        # Lets check the integrity of each message. If the
        # integrity is not successfully verified, remove the
        # message from the array messages.
        for m in messages:
            data_len = m[1]
            if len(m) != data_len + 2:
                messages.remove(m)

        # If the array of messages has only one object return
        # only this single element rather than a list with a
        # single element:
        #if 1 == len(messages):
        #    messages = messages[0]

        # If messages is empty than set it to None
        if [] == messages:
            messages = None

        return messages

    def _bytearr2str(self, bytearr=None):
        """
        Converts a bytearray to a string

        Records in the module can be labelled with signatures. Signatures are
        returned by the module as bytearrays. This method helps to convert them
        to string variables that can be used e.g. by ``print()``.

        Parameters:
            bytearr (bytearray or None): bytearray representing e.g. a record signature

        Returns:
            retstr (str or None): string variable converted from ``bytearr``. In case
                ``bytearr`` is ``None`` ``None`` will be returned.
        """

        if None != bytearr:
            retstr = ""
            for b in bytearr:
                retstr += chr(b)
        else:
            retstr = None

        return retstr

    def _default_callback(self, response_dict):
        """
        Default callback function for ``record_recognized()``

        This callback function can be called every time a response message from
        the recognizer of the module is received. It accepts a dictionary
        containing the response message and outputs some details to the screen.

        Parameters:
            response_dict (dict): dictionary containing the response message
                from the module

        Returns:
            Nothing
        """

        if None != response_dict["signature_recognized_record"]:
            sign = (" ("
                + response_dict["signature_recognized_record"]
                + ")"
                )
        else:
            sign = ""
        print("Recognized record %d%s at time %f."
            % (response_dict["recognized_record"],
            sign,
            response_dict["time_passed_ms"])
            )

    def send_cmd(self, command):
        """
        Sending a command to the module and receiving response(s)

        Parameters:
            command (bytearray): command to be sent to the module

        Returns:
            messages (array of bytearray): response messages from
                the module
        """

        self._send_cmd(command)
        messages = self._recv_rsp()
        return messages

    def check_system_settings(self):
        """
        Checks system settings (00)

        The method returns a dictionary containing the response from the
        module:

            response_dict = {
                    "raw": response_bin,
                    "trained": sta,
                    "rec_value_out_of_range": rverr,
                    "baudrate": br,
                    "output_io_mode": iom,
                    "output_io_pulse_width_ms": iopw,
                    "autoload": al,
                    "group_control": grp,
                    }

        Parameters:
            None

        Returns:
            response (dict): dictionary containing the response
                from the module
        """

        # Compile and send command; return respoonse from module
        command = self._compile_cmd(payload = b'\x00')
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = None

        if None != response_bin:
            # The response from the module will always contain
            # one single message
            if 1 == len(response_bin):
                response_bin = response_bin[0]

                # Training status and record value out of range
                if 0 == response_bin[3]:
                    sta = False
                    rverr = False
                elif 1 == response_bin[3]:
                    sta = True
                    rverr = False
                elif  255 == response_bin[3]:
                    sta = None
                    rverr = True
                else:
                    sta = None
                    rverr = None

                # Baudrate
                # Look up value in list br_conv
                try:
                    br = br_conv[response_bin[4]]
                except:
                    br = None

                # Output IO mode
                try:
                    iom = iomode_conv[response_bin[5]]
                except:
                    iom = None

                # IOPW: Output IO Pulse Width (Pulse Mode)
                # Get pulse width length in milliseconds by looking up in
                # the list iopw_conv:
                try:
                    iopw = iopw_conv[response_bin[6]]
                except:
                    iopw = None

                # Power on auto load
                if 0 == response_bin[7]:
                    al = False
                elif 1 == response_bin[7]:
                    al = False
                else:
                    al = None

                #GRP: Group control by external IO
                if 0 == response_bin[8]:
                    grp = "disabled"
                elif 1 == response_bin[8]:
                    grp = "system group"
                elif 2 == response_bin[8]:
                    grp = "user group"
                else:
                    grp = None

                # Compile dictionary with response from module
                response_dict = {
                        "raw": response_bin,
                        "trained": sta,
                        "rec_value_out_of_range": rverr,
                        "baudrate": br,
                        "output_io_mode": iom,
                        "output_io_pulse_width_ms": iopw,
                        "autoload": al,
                        "group_control": grp,
                        }

        return response_dict

    def check_recognizer(self):
        """
        Checks recognizer (01)

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                    "raw": response_bin,
                    "no_records_in_recognizer": rvn,
                    "records_in_recognizer": vri_dec,
                    "group_mode": grpm,
                    }

        Parameters:
            None

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Compile and send command; read response from module
        command = self._compile_cmd(payload = b'\x01')
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = None

        if None != response_bin:
            # The response from the module will always contain
            # one single message
            if 1 == len(response_bin):
                response_bin = response_bin[0]
                # Number of valid records in recognizer (max 7)
                rvn = response_bin[3]

                # Record values in recognizer
                vri = response_bin[4:12]
                vri_dec = []
                for i in range(len(vri) - 1):
                    vri_dec.append(vri[i])

                # Group mode indicator
                if 255 == response_bin[11]:
                    grpm = "not in group mode"
                # ToDo: Check if return value \x00 exists. Docu unclear
                #
                #elif 0 == response_bin[11]:
                #    grpm = "system group mode"
                elif 135 == response_bin[11]:
                    grpm == "user group mode"
                else:
                    grpm = None

                # Compile dictionary with response from module
                response_dict = {
                        "raw": response_bin,
                        "no_records_in_recognizer": rvn,
                        "records_in_recognizer": vri_dec,
                        "group_mode": grpm,
                        }

        return response_dict

    def check_record_train_status(self, record=None):
        """
        Checks record train status (02)

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                    "raw": response_bin,
                    "no_trained_records": n,
                    "trained_records": rec,
                    "train_status": sta,
                    }
        Parameters:
            record (None or int): record number to be checked. If None,
                all records will be checked.

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Compile the command payload (data) from the function's
        # arguments
        payload = bytearray(b'\x02')
        # Append record number to cmd payload
        if None != record:
            payload.append(record)
        else:
            # Check status for all records
            payload.append(255)

        # Compile and send command; read response from module
        command = self._compile_cmd(payload = payload)
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = None

        if None != response_bin:
            # Loop over all messages

            # Initialize lists to collect results from the messages
            # in the response from the module
            rec = []    # Record numbers
            sta = []    # Record status

            # Loop over all messages and fill above lists
            for resp in response_bin:
                # The total number of trained records is repeated
                # in every message. It makes no difference from
                # which message we extract this info.
                n = resp[3]
                # Length of data/payload of message
                nr = int((len(resp) - 5)/ 2)
                # Extract data
                for i in range(nr):
                    rec.append(resp[4 + 2*i])
                    if 0 == resp[5 + 2*i]:
                        sta.append("untrained")
                    elif 1 == resp[5 + 2*i]:
                        sta.append("trained")
                    elif 255 == resp[5 + 2*i]:
                        sta.append("out of range")
                    else:
                        sta.append("unknown")

            # Compile dictionary with response from module
            response_dict = {
                    "raw": response_bin,
                    "no_trained_records": n,
                    "trained_records": rec,
                    "train_status": sta,
                    }

        return response_dict

    def check_record_signature(self, record=None):
        """
        Check the signature of a record (03)

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                "record": record,
                "signature": signature,
                    }

        The signature for a record (optional) can be considered as a "label"
        for the record. In principle, the module allows any ASCII character
        with ASCII code < 255. The maximum number of characters for the
        signature is 26 (derived from test on module V3.1). To avoid any
        potential problems the character range is limited from "!" (ASCII 33)
        to "~" (ASCII 126).

        Parameters:
            record (int): Record number

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Initialize response dict
        response_dict = None

        # Proceed only if record number was given
        if None != record:
            # If this method is applied to a record that is not trained and has
            # no signature it will not return meaningful results. The signature
            # returned by the module will contain some random characters. This
            # is an issue of the module. Therefore, as a first step determine
            # the traning status of the record. Only, if the record is trained
            # ask the module for the signature.

            # Get training status for the record
            sta = self.check_record_train_status(record)["train_status"][0]

            if "trained" == sta:
                # Compile the command payload (data)
                payload = bytearray(b'\x03')
                payload.append(record)

                # Compile and send command; read response from module
                command = self._compile_cmd(payload = payload)
                self._send_cmd(command)
                response_bin = self._recv_rsp()

                # Initialize dict for return value of this function
                response_dict = None

                if None != response_bin:
                    # The response from the module will always contain
                    # one single message
                    if 1 == len(response_bin):
                        response_bin = response_bin[0]

                        # Compile dictionary with response from module
                        sign = self._bytearr2str(response_bin[5:-1])
                        response_dict = {
                                "raw": response_bin,
                                "record": record,
                                "signature": sign,
                                }
            else:
                # For untrained records no meaningful response from the module
                # can be retrieved
                response_dict = {
                        "raw": None,
                        "record": record,
                        "signature": None,
                        }

        return response_dict

    def restore_system_settings(self):
        """
        Restore the system settings of the module to defaults (10)

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                    }

        Parameters:
            None

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Compile the command payload (data)
        payload = bytearray(b'\x10')

        # Compile and send command; read response from module
        command = self._compile_cmd(payload = payload)
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = {
            "raw": response_bin,
                }

        return response_dict

    def set_baudrate(self, baudrate=None):
        """
        Set the baud rate of the module (11)

        The following baud rates are supported by the module:

        * 2400 baud
        * 4800 baud
        * 9600 baud
        * 19200 baud
        * 38400 baud

        The change of baudrate takes effect only after restarting the module.

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                    }

        Parameters:
            baudrate (int): baud rate

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module

        Raises:
            BadBaudrate: When no or an unsupported baud rate is given
        """

        # Check if we were called with a valid baudrate value. If not raise
        # BadBaudrate exception
        if None != baudrate and isinstance(baudrate, int):
            if (baudrate in br_conv):
                # When this for-loop exits it provides the index value in the
                # list br_conv (br) that will be used below to compile the
                # command's payload
                for br in range(len(br_conv)):
                    if br_conv[br] == baudrate:
                        break
            else:
                raise BadBaudrate
        else:
            raise BadBaudrate

        # Compile the command payload (data)
        payload = bytearray(b'\x11')
        # Here we use br from above
        payload.append(br)

        # Compile and send command; read response from module
        command = self._compile_cmd(payload = payload)
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = {
            "raw": response_bin,
            "baudrate": baudrate,
                }

        return response_dict


    def set_output_io_mode(self, mode=None):
        """
        Set the output IO mode (12)

        The output IO mode determines how the output pins of the module (OUT0
        ... OUT6) behave in case the module recognizes a voice command. The
        output pins represent the 7 records in the recognizer. For example, if
        the third record in the recognizer is recognized only OUT2 will be
        affected. There are 4 different modes:

        0 -- Pulse: Send negative pulse to output. The pulse width can be
             configured with the method set_output_io_pulse_width().
        1 -- Toggle: Toggle the output state each time a recognition takes
             place.
        2 -- Set: Set output to high when the module recognizes a voice
             command. The ouput state will stay high until the state is
             resetted with the method reset_output_io().
        2 -- Clear: Set output to low when the module recognizes a voice
             command. The ouput state will stay low until the state is
             resetted with the method reset_output_io().

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                "output_io_mode": output io mode,
                    }

        Parameters:
            mode (str): Output IO mode ("pulse", "toggle", "set", "clear")

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module

        Raises:
            BadMode: When no or an unsupported output IO mode is given
        """

        # Check if we were called with a valid mode
        if None != mode and isinstance(mode, str):
            mode = mode.lower()
            if (mode in iomode_conv):
                # When this for-loop exits it provides the index value in the
                # list iomode_conv (m) that will be used below to compile the
                # command's payload
                for m in range(len(iomode_conv)):
                    if iomode_conv[m] == mode:
                        break
            else:
                raise BadMode
        else:
            raise BadMode

        # Compile the command payload (data)
        payload = bytearray(b'\x12')
        # Here we use m from above
        payload.append(m)

        # Compile and send command; read response from module
        command = self._compile_cmd(payload = payload)
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = {
            "raw": response_bin,
            "output_io_mode": mode,
                }

        return response_dict

    def set_output_io_pulse_width(self, pulsewidth=None):
        """
        Set output IO pulse width (13)

        The method sets the output io pulse width of the module. It takes
        effect directly after the execution of the command.

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                "output_io_pulse_width_hex": hex value for pulsewidth,
                "output_io_pulse_width_ms": pulsewidth in ms,
                    }

        Parameters:
            pulsewidth (int): Pulse width in milliseconds. Only sepcific values
                are allowed: 10, 15, 20, 25, 30, 35, 40, 45, 50, 75, 100, 200,
                300, 400, 500, 1000 ms.

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module

        Raises:
            BadPulseWidth: pulse width wrong or unsupported
        """

        # Check if we were called with a valid pulse width
        if None != pulsewidth and isinstance(pulsewidth, int):
            if (pulsewidth in iopw_conv):
                # When this for-loop exits it provides the index value in the
                # list iopw_conv (pw) that will be used below to compile the
                # command's payload
                for pw in range(len(iopw_conv)):
                    if iopw_conv[pw] == pulsewidth:
                        break
            else:
                raise BadPulseWidth
        else:
            raise BadPulseWidth

        # Compile the command payload (data)
        payload = bytearray(b'\x13')
        # Here we use pw from above
        payload.append(pw)

        # Compile and send command; read response from module
        command = self._compile_cmd(payload = payload)
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = {
            "raw": response_bin,
            "output_io_pulse_width_hex": hex(pw),
            "output_io_pulse_width_ms": pulsewidth,
                }

        return response_dict

    def reset_output_io(self, *outn):
        """
        Reset output IO (14)

        Resets the state of selected or all output IO pins.

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                "output_io_resetted": sorted list of pins that were resetted,
                    }

        Parameters:
            outn (list of int or None): output io pins to be resetted. If no
                pin is specified all output pins will be resetted. All pins
                have to be in the range 0...6 and correspond to the places in
                the recognizer.

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module

        Raises:
            BadIOPin: output pin wrong or unsupported
        """

        payload = bytearray(b'\x14')
        pins = []

        # Check output io pins provided
        if () == outn:
            # If no argument is given (empty list) reset all io pins
            pins = list(range(7))
        else:
            # Iterate over outn
            for o in outn:
                # Pins shall be specified as integers
                if not isinstance(o,int):
                    raise BadIOPin
                else:
                    # Valid pin numbers only in range 0...6
                    if o < 0 or o > 6:
                        raise BadIOPin
                    else:
                        pins.append(o)

                # len(pins) shall never be greater than 7
                if len(pins) > 7:
                    raise BadIOPin
        # Compile and send command; read response from module
        for p in range(len(pins)):
            payload.append(pins[p])
        command = self._compile_cmd(payload = payload)
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = {
            "raw": response_bin,
            "output_io_resetted": sorted(pins),
                }

        return response_dict

    # set_power_on_auto_load (15)

    def train_record(self, record=None, signature=None):
        """
        Train a record without (20) or with signature (21)

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                "record": record,
                "signature": signature,
                "training_status": sta
                    }

        The signature for a record (optional) can be considered as a "label"
        for the record. In principle, the module allows any ASCII character
        with ASCII code < 255. The maximum number of characters for the
        signature is 26 (derived from test on module V3.1). To avoid any
        potential problems the character range is limited from "!" (ASCII 33)
        to "~" (ASCII 126).

        Parameters:
            record (int): Record number to train
            signature (str or None): Signature for record

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module

        Raises:
            BadSignature: signature is too long or contains bad characters
        """

        # Code from elechouse Arduino library
        #  train method: https://github.com/elechouse/VoiceRecognitionV3/blob/964d022b81b154b0fc5699e624d38e323915487b/VoiceRecognitionV3.cpp#L95

        # Initialize response dict
        response_dict = None

        # Check for "good signature"
        if None != signature:
            # 1) Length of signature
            if len(signature) > sign_max_len:
                raise BadSignature
            # 2) Search for bad characters
            for c in range(len(signature)):
                if ord(signature[c]) < sign_char_min_ascii or ord(signature[c]) > sign_char_max_ascii:
                    raise BadSignature

        # Proceed only if record number was given
        if None != record:
            # Compile the command payload (data) from the function's
            # arguments. If no signature is provided use command 20, else
            # command 21
            if None == signature:
                # No signature => command 20
                payload = bytearray(b'\x20')
                # Append record number to cmd payload
                payload.append(record)
            else:
                # Signature => command 21
                payload = bytearray(b'\x21')
                # Append record number to cmd payload
                payload.append(record)
                # Append characters of signature as ASCII codes
                for c in range(len(signature)):
                    payload.append(ord(signature[c]))

            # Compile and send command
            command = self._compile_cmd(payload = payload)
            self._send_cmd(command)

            dialog_tout = 8             # timeout for dialog with module
                                        # in seconds
            tick = time.time()          # start time for timeout watchdog
            train_finished = False      # indicator if training finished

            # Loop until dialog timeout or training is finished
            while (time.time() - tick < dialog_tout or train_finished):
                # Read data from module
                response_bin = self._recv_rsp()

                # There are two response types
                #  1) prompt msg: b'\xaa\[l]\x0a\[rec]\[prompt]\x0a'
                #  2) status msg: b'\xaa\[l]\x20\[num]\[rec]\[sta]\[sig]\x0a'

                if None != response_bin:
                    if 1 == len(response_bin):
                        # Reset timeout watchdog
                        tick = time.time()

                        response_bin = response_bin[0]
                        #print(response_bin)

                        # Prompt message
                        if 10 == response_bin[2]:       # \x0a
                            msg = response_bin[4:-1]    # msg
                            msg = self._bytearr2str(msg)
                            print("Record", record, ":\t", msg)

                        # Status message (20: train w/o signature)
                        if 32 == response_bin[2]:       # \x20
                            # Status message ends training
                            train_finished = True
                            sta = response_bin[5]       # train status
                            print("Training ended.\t", sta)

                            response_dict = {
                                "raw": response_bin,
                                "record": record,
                                "signature": None,
                                "training_status": sta
                                    }

                        # Status message (21: train with signature)
                        if 33 == response_bin[2]:       # \x20
                            # Status message ends training
                            train_finished = True
                            sta = response_bin[5]       # train status
                            print("Training ended.\t", sta)

                            response_dict = {
                                "raw": response_bin,
                                "record": record,
                                "signature": signature,
                                "training_status": sta
                                    }

        return response_dict

    def set_signature(self, record=None, signature=None):
        """
        Set signature for record (22)

        The signature for a record (optional) can be considered as a "label"
        for the record. In principle, the module allows any ASCII character
        with ASCII code < 255. The maximum number of characters for the
        signature is 26 (derived from test on module V3.1). To avoid any
        potential problems the character range is limited from "!" (ASCII 33)
        to "~" (ASCII 126).

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                "raw": response_bin,
                "record": record,
                "signature": signature,
                    }

        Parameters:
            record (int): Record number to train
            signature (str or None): Signature for record

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module

        Raises:
            BadSignature: signature is too long or contains bad characters
        """

        # Initialize response dict
        response_dict = None

        # Check for "good signature"
        if None != signature:
            # 1) Length of signature
            if len(signature) > sign_max_len:
                raise BadSignature
            # 2) Search for bad characters
            for c in range(len(signature)):
                if ord(signature[c]) < sign_char_min_ascii or ord(signature[c]) > sign_char_max_ascii:
                    raise BadSignature

        # Proceed only if record number was given
        if None != record:
            # Compile the command payload (data) from the function's
            # arguments.
            if None == signature:
                signature = ""

            payload = bytearray(b'\x22')
            # Append record number to cmd payload
            payload.append(record)
            # Append characters of signature
            for c in range(len(signature)):
                payload.append(ord(signature[c]))

            # Compile and send command. Read response from module
            command = self._compile_cmd(payload = payload)
            self._send_cmd(command)
            response_bin = self._recv_rsp()

            response_dict = {
                "raw": response_bin,
                "record": record,
                "signature": signature,
                    }

        return response_dict

    def load_to_recognizer(self, *records):
        """
        Load record(s) to recognizer (30)

        The method returns a dictionary containing the response message from
        the module:

            response_dict = {
                    "raw": response_bin,
                    "no_records_in_recognizer": n,
                    "records_in_recognizer": rec,
                    "status": sta,
                    }

        Parameters:
            records (int): Record number(s) to be loaded
                to recognizer.

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Initialize response dict
        response_dict = None

        # Proceed only if record number was given
        if None != records:
            # Compile the command payload (data) from the function's
            # arguments
            payload = bytearray(b'\x30')
            # Append record number(s) to cmd payload
            if hasattr(records, "__iter__"):
                for r in records:
                    payload.append(r)
            else:
                payload.append(records)

            # Compile and send command; read response from module
            command = self._compile_cmd(payload = payload)
            self._send_cmd(command)
            response_bin = self._recv_rsp()

            if None != response_bin:
                # Loop over all messages

                # Initialize lists to collect results from the messages
                # in the response from the module
                rec = []    # Record numbers
                sta = []    # Record status

                # Loop over all messages and fill above lists
                for resp in response_bin:
                    # The total number of records in recognizer is
                    # repeated in every message. It makes no difference
                    # from which message we extract this info.
                    n = resp[2]
                    # Length of data/payload of message
                    nr = int((len(resp) - 5)/ 2)
                    # Extract data
                    for i in range(nr):
                        rec.append(resp[4 + 2*i])
                        if 0 == resp[5 + 2*i]:
                            sta.append("success")
                        elif 255 == resp[5 + 2*i]:
                            sta.append("out of range")
                        elif 254 == resp[5 + 2*i]:
                            sta.append("record untrained")
                        elif 253 == resp[5 + 2*i]:
                            sta.append("recognizer full")
                        elif 252 == resp[5 + 2*i]:
                            sta.append("already in recognizer")
                        else:
                            sta.append("unknown")
                        sta.append(resp[5 + 2*i])

                # Compile dictionary with response from module
                response_dict = {
                        "raw": response_bin,
                        "no_records_in_recognizer": n,
                        "records_in_recognizer": rec,
                        "status": sta,
                        }

        return response_dict


    def clear_recognizer(self):
        """
        Clear recognizer and stop recognizing (31)

        The method returns a dictionary containing the response message from
        the module:

            response_dict = { "status": sta }

        Parameters:
            None

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Compile and send command; return respoonse from module
        command = self._compile_cmd(payload = b'\x31')
        self._send_cmd(command)
        response_bin = self._recv_rsp()

        # Initialize dict for return value of this function
        response_dict = None

        if None != response_bin:
            # The response from the module will always contain
            # one single message
            if 1 == len(response_bin):
                response_bin = response_bin[0]
                sta = response_bin[3]

                response_dict = { "status": sta }

        return response_dict

    # group_control (32)

    def record_recognized(self, timeout=None, callback_func=None):
        """
        Wait until trained record is recognized (0d)

        This method requires that at least one record is loaded to the
        recognizer of the module. It waits until ``timeout`` for a response
        message indicating that the module recognized a voice input.

        A callback function can be defined by ``callback_func``. If no custom
        callback function is provided (``None``) the default callback function
        ``_default_callback`` is used.
        module. The dictionary for the response has the following keys:

        * raw (bytearray): raw message from module
        * time_passed_ms (float): time of recognition in miliseconds after invocation
          of method ``record_recognized()``
        * records_in_recognizer (array of int): list of records in recognizer
        * recognized_record (int): the record number of the recognized record
        * index_recognized_record (int): index of the recognized record in the
          recognizer
        * signature_recognized_record (str or None): signature of the recognized
          record if present, otherwise ``None``
        * group_mode (int or None): group mode of module

        A sample custom callback function could look like:

            def custom_callback_function(response):
                print("Recognized something!")
                for key, value in response.items():
                    print("  ", key, value)
                print("")

        Parameters:
            timeout (int): Timeout in milliseconds to wait for
                a recognition
            callback_func (Name of callback function or None): Name
                of callback function to call when record is recognized.

        Returns:
            Nothing
        """

        # Initialize dictionary for response
        response_dict = {
                "raw": None,
                "time_passed_ms": None,
                "records_in_recognizer": None,
                "recognized_record": None,
                "index_recognized_record": None,
                "signature_recognized_record": None,
                "group_mode": None,
                }

        # First check status of recognizer. At least one record
        # has to be loaded to recognizer.
        status_recognizer = self.check_recognizer()
        if status_recognizer["no_records_in_recognizer"] > 0:
            # Populate some values in response_dict
            response_dict["records_in_recognizer"] = status_recognizer["records_in_recognizer"]
            response_dict["group_mode"] = status_recognizer["group_mode"]

            if None == timeout:
                # Set timeout to practically infinite
                timeout = 10**10       # corresponds to ~ 3 years

            # Default for time_passed_ms in response_dict is
            # timeout:
            response_dict["time_passed_ms"] = timeout

            # Check argument callback_func
            if None == callback_func:
                # Set to default callback function
                callback_func = self._default_callback

            # No nead to send any command. Just wait for the module
            # to send something
            start = time.time()
            while (1000 * (time.time() - start) < timeout):
                # Read response from module
                response_bin = self._recv_rsp(latency = 0)
                if None != response_bin:
                    # We expect a single message
                    if 1 == len(response_bin):
                        response_bin = response_bin[0]
                        # Proceed only if correct message type
                        if 13 == response_bin[2]:      # \x0d
                            response_dict["raw"] = response_bin
                            response_dict["time_passed_ms"] = 1000 * (time.time() - start)
                            response_dict["recognized_record"] = response_bin[5]
                            response_dict["index_recognized_record"] = response_bin[6]
                            sig = response_bin[8:-1]
                            sigstr = self._bytearr2str(sig)
                            if "" == sigstr:
                                sigstr = None
                            response_dict["signature_recognized_record"] = sigstr

                            # Execute callback function
                            callback_func(response_dict)

                # Reduce "speed" of while loop to reduce cpu usage
                time.sleep(0.05)


