import serial
import time

# Elechouse Voice Recognition Module V3*
# Protocol definition see:
# https://github.com/elechouse/VoiceRecognitionV3#protocol

# List to convert hex value for IO pulse width to milliseconds
iopw_conv = (10, 15, 20, 25, 30, 35, 40, 45, 50, 75, 100,
        100, 300, 400, 500, 1000)

class PyVoiceRecognitionV3:

    def __init__(self,
            port='/dev/ttyUSB0',        # Serial port
            baudrate=9600,              # Baudrate
        # Even for the lowest baudrate possible (2400 baud)
        # transmitting one byte should not take longer than
        # 10 ms. If after this time we get no more byte than
        # assume all bytes of a response are transmitted.
            tout=10,                    # Timeout in ms
            ):
        self.port = port
        self.baudrate = baudrate
        self.tout = tout

        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def __compile_cmd(self, payload):
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

    def __send_cmd(self, command):
        # Before sending a new command clear the input buffer
        self.ser.reset_input_buffer()
        self.ser.write(command)

    def __recv_rsp(self, tout=None):
        if None == tout:        # Timeout in ms
            tout = self.tout

        # Initialize array for byte stream from module
        response = bytearray()

        # Read byte by byte until timeout (tout) is
        # reached
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

    def __bytearr2str(self, bytearr=None):
        if None != bytearr:
            retstr = ""
            for b in bytearr:
                retstr += chr(b)
        else:
            retstr = None

        return retstr

    def send_cmd(self, command):
        self.__send_cmd(command)
        messages = self.__recv_rsp()
        return messages

    def check_system_settings(self):
        """
        Checks System Settings (00)

        Parameters:
            None

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Compile and send command; return respoonse from module
        command = self.__compile_cmd(payload = b'\x00')
        self.__send_cmd(command)
        response_bin = self.__recv_rsp()

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
                if 0 == response_bin[4] or b'\x03' == response_bin[4]:
                    br = 9600
                elif 1 == response_bin[4]:
                    br = 2400
                elif 2 == response_bin[4]:
                    br = 4800
                elif 4 == response_bin[4]:
                    br = 19200
                elif 5 == response_bin[4]:
                    br = 38400
                else:
                    br = None

                # Output IO mode
                if 0 == response_bin[5]:
                    iom = "pulse"
                elif 1 == response_bin[5]:
                    iom = "toggle"
                elif 2 == response_bin[5]:
                    iom = "clear"
                elif 3 == response_bin[5]:
                    iom = "set"
                else:
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
        Checks Recognizer (01)

        Parameters:
            None

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Compile and send command; read response from module
        command = self.__compile_cmd(payload = b'\x01')
        self.__send_cmd(command)
        # I discovered that after clearing the recognizer it takes at
        # least two attempts to get a status response from the
        # recognizer. Retry reading a response != None 3 times.
        max_iter = 3
        response_bin = None
        while None == response_bin and max_iter > 0:
            response_bin = self.__recv_rsp()

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
                        "valid_rec_in_recognizer": rvn,
                        "records_in_recognizer": vri_dec,
                        "group_mode": grpm,
                        }

        return response_dict

    def check_record_train_status(self, record=None):
        """
        Checks Record Train Status (02)

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
        command = self.__compile_cmd(payload = payload)
        self.__send_cmd(command)
        response_bin = self.__recv_rsp()

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
                n = resp[2]
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
                    "trained_records": n,
                    "records": rec,
                    "train_status": sta,
                    }

        return response_dict

    def train_record(self, record=None):
        """
        Train a record (20)

        Parameters:
            record (int): Record number to train

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        # Code from elechouse Arduino library
        #  train method: https://github.com/elechouse/VoiceRecognitionV3/blob/964d022b81b154b0fc5699e624d38e323915487b/VoiceRecognitionV3.cpp#L95

        # Initialize response dict
        response_dict = None

        # Proceed only if record number was given
        if None != record:
            # Compile the command payload (data) from the function's
            # arguments
            payload = bytearray(b'\x20')
            # Append record number to cmd payload
            payload.append(record)

            # Compile and send command
            command = self.__compile_cmd(payload = payload)
            self.__send_cmd(command)

            dialog_tout = 8             # timeout for dialog with module
                                        # in seconds
            tick = time.time()          # start time for timeout watchdog
            train_finished = False      # indicator if training finished

            # Loop until dialog timeout or training is finished
            while (time.time() - tick < dialog_tout or train_finished):
                # Read data from module
                response_bin = self.__recv_rsp()

                # There are two response types
                #  1) prompt msg: b'\xaa\[l]\x0a\[rec]\[prompt]\x0a'
                #  2) status msg: b'\xaa\[l]\x20\[num]\[rec]\[sta]\[sig]\x0a'

                if None != response_bin:
                    if 1 == len(response_bin):
                        # Reset timeout watchdog
                        tick = time.time()

                        response_bin = response_bin[0]
                        print(response_bin)

                        # Prompt message
                        if 10 == response_bin[2]:       # \x0a
                            msg = response_bin[4:-1]    # msg
                            msg = self.__bytearr2str(msg)
                            print("Record", record, ":\t", msg)

                        # Status message
                        if 32 == response_bin[2]:       # \x20
                            # Status message ends training
                            train_finished = True
                            sta = response_bin[5]       # train status
                            print("Training ended.\t", sta)

                            response_dict = {
                                "raw": response_bin,
                                "record": record,
                                "training_status": sta
                                    }
        return response_dict

    def load_to_recognizer(self, *records):
        """
        Load record(s) to recognizer (30)

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
            command = self.__compile_cmd(payload = payload)
            self.__send_cmd(command)
            response_bin = self.__recv_rsp()

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
                        "records_in_recognizer": n,
                        "records": rec,
                        "status": sta,
                        }

        return response_dict


    def clear_recognizer(self):
        """
        Clear recognizer and stop recognizing (31)

        Parameters:
            None

        Returns:
            None
        """

        # Compile and send command; return respoonse from module
        command = self.__compile_cmd(payload = b'\x31')
        self.__send_cmd(command)
        response_bin = self.__recv_rsp()

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
