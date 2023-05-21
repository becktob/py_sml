import re

import serial

if __name__ == '__main__':
    port = '/dev/ttyAMA0'
    serialPort = serial.Serial(port, 9600,
                               bytesize=serial.EIGHTBITS, # 8-N-1
                               parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE,
                               timeout=5)

    while True:
        data = serialPort.read(5640)
        print(data)
        message = re.findall(b'\x1b\x1b\x1b\x1b\x01\x01\x01.*', data)
        if message:
            message = message[0]
            print(f"{len(data)=}")
            print(message)
            TT = message[8]
            send = (TT & 0b1000_0000) == 0
            print(f"TT: {send=}")

