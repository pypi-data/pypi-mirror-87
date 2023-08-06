from time import sleep

import serial
import logging

logger = logging.getLogger(__name__)


class Sniffer:
    def __init__(self, com_listener, com_sender):
        self.com_listener = com_listener
        self.com_sender = com_sender

    def connect(self):
        ser = serial.Serial(
            port=self.com_listener,
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=5
        )
        self.ser_listener = ser
        self.ser_listener.flushInput()

        ser = serial.Serial(
            port=self.com_sender,
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=5
        )
        self.ser_sender = ser
        self.ser_sender.flushInput()

    def write(self, ser, data: bytes = None):
        """Write bytes to serial port"""

        # logger.debug(f"Data sent: {data}")
        if data:
            try:
                ser.write(data)
            except serial.SerialException as e:
                logger.warning(e)
                raise

    def read(self, ser, last_char=b'\x83'):
        """Read from serial 1 byte at a time. Stop when last_char is received."""

        frame = b""
        while True:
            try:
                byte = ser.read(1)
            except serial.SerialException as e:
                logger.warning(e)
                raise
            if byte:
                frame += byte
                if byte == last_char:
                    break
            else:
                break
        logger.debug(f"Data received: {frame}")
        return frame

    def start(self):
        """Reroute serial port from listener to sender"""
        i = 0
        while True:
            # Read from first serial port
            frame = self.read(self.ser_listener)
            logger.debug(frame)
            self.write(self.ser_sender, frame)
            frame1 = self.read(self.ser_sender)
            self.write(self.ser_listener, frame1)
            if 'SCWD' in str(frame):
                sleep(31)
            if 'CTFR' in str(frame):
                with open('raw_send_jaro', 'a+') as f:
                    f.write(repr(frame) + "\n")
                with open('raw_receive_jaro', 'a+') as f:
                    f.write(repr(frame1) + "\n")
                i += 1
            print (i)

def main():
    s = Sniffer(com_listener='COM7', com_sender='COM5')
    s.connect()
    s.start()

if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=formatter)
    logging.root.setLevel('DEBUG')
    main()

