import logging
import re
import time

import serial

from SML_binary import parse_binary_SML_message_from_stream
from SML_message import SmlMessage

def raw_message_from_port(serial_port: serial.Serial):
    buffer = bytearray()
    tic = time.time()
    while True:
        buffer += serialPort.read(serial_port.inWaiting())

        end = re.search(end_of_message, buffer)
        if end:
            last_byte=end.span()[1]
            ret = buffer[:last_byte]
            buffer = buffer[last_byte:]

            toc = time.time()
            logging.info(f"got {len(ret)} bytes in {toc-tic:.1f} s at {8 * len(ret) / (toc - tic):.1f} bit/s")
            tic = time.time()
            yield ret

if __name__ == '__main__':
    end_of_message = b'\x1b\x1b\x1b\x1b\x1a.{3}'

    port = '/dev/ttyAMA0'
    serialPort = serial.Serial(port, 9600,
                               bytesize=serial.EIGHTBITS, # 8-N-1
                               parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE,
                               timeout=2)

    for raw_message in raw_message_from_port(serialPort):

        sml_token_messages = parse_binary_SML_message_from_stream(raw_message)

        try:
            if sml_token_messages:
                for token_message in sml_token_messages:
                    sml_message = SmlMessage.parse_from_tokens(token_message)
                    if sml_message and sml_message.message_body:
                        for val in sml_message.message_body.val_list:
                            if val.display_name and "power" in val.display_name:
                                print(val)
        except:
            logging.exception("somethint went wrong.")

