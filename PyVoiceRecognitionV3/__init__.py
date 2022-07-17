import serial
import time
import binascii

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
        self.ser.write(command)
        response = bytearray()

        # Read byte by byte until timeout (self.tout) is
        # reached
        last = time.time()
        while ((time.time() - last) < self.tout/1000.):
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

        # If response from the module is already less than 4 bytes
        # we can absolutely have no valid message at all. In this
        # case we do not need to go through the following while
        # loop.
        if len(response) >= 3:
            end_of_resp = False
        else:
            end_of_resp = True

        p = 0   # Position of "pointer" in response
        while not end_of_resp:
            # If necessary move p to the first occurance of \xaa or
            # 170 (decimal)
            while response[p] != 170:
                p += 1
                # The minimum-length message has 3 bytes:
                # \xaa\x01\x0a
                if not p < len(response) - 3:
                    end_of_resp = True
                    break

            # If a valid message starts at current position p at
            # position (p+1) should be the length of the message
            # without header field (\xaa) and end field (\x0a).
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
        if 1 == len(messages):
            messages = messages[0]

        # If messages is empty than set it to None
        if [] == messages:
            messages = None

        return messages

    def send_cmd(self, command):
        messages = self.__send_cmd(command)
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

        command = self.__compile_cmd(payload = b'\x00')
        response_bin = self.__send_cmd(command)
        if None != response_bin:
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

        command = self.__compile_cmd(payload = b'\x01')
        response_bin = self.__send_cmd(command)

        if None != response_bin:
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

    def check_record_train_status(self, records=None):
        """
        Checks Record Train Status (02)

        Parameters:
            records (list of int): List of records to be checked

        Returns:
            response (dict): dictionary containing the response
                from the voice recognition module
        """

        payload = bytearray(b'\x02')
        # Append record or list of records to cmd payload if exists
        if not None == records:
            if hasattr(records, '__iter__'):
                for r in records:
                    payload.append(r)
            else:
                # Assume single record to be added to the cmd payload
                payload.append(records)
        else:
            # Check status for all records
            payload.append(255)
        command = self.__compile_cmd(payload = payload)
        print(command)

        responses = self.__send_cmd(command)

        if not None == responses:

            # ToDo: The following if clause does not work
            if hasattr(responses, '__iter__'):
                print(responses)
                # Number of trained records is repeated in every
                # message. Therefore, we can pick it out of the
                # first message
                n = responses[0][3]

                # Record train status
                rec = []    # Record number
                sta = []    # Record status
                for resp in responses:
                    nr = int((len(resp) - 5)/ 2)
                    for i in range(nr):
                        rec.append(resp[4 + 2*i])
                        sta.append(resp[5 + 2*i])
            else:
                # Number of trained records
                n = responses[3]

                # Record train status
                rec = []    # Record number
                sta = []    # Record status
                nr = int((len(responses) - 5)/ 2)
                for i in range(nr):
                    rec.append(responses[4 + 2*i])
                    sta.append(responses[5 + 2*i])

            # Compile dictionary with response from module
            response_dict = {
                    "raw": responses,
                    "trained_records": n,
                    "records": rec,
                    "train_status": sta,
                    }

            return response_dict

#cmd=binascii.a2b_hex('aa0303010a')
#ser.write(cmd)
#
#b=''
#while b != b'\n':
#    if ser.inWaiting():
#        b = ser.read(1)
#        print(binascii.b2a_hex(b))
