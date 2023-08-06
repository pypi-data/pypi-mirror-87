from time import sleep

from serial import SerialException
from serial.tools import list_ports
import serial
import logging


logger = logging.getLogger(__name__)


def comports():
    """Return list of available comports"""

    available_ports = []
    ports = list_ports.comports()
    for port in ports:
        available_ports.append(str(port))
    return available_ports


def serial_ports():
    """Filter serial ports from all comports and strip away description of port"""

    ports = comports()
    ser_ports = list(filter(lambda x: 'Serial Port' in x, ports))
    ser_ports = [i.split(' ')[0] for i in ser_ports]
    return ser_ports


def autodetermine_port():
    """Auto select first serial port"""

    ser_ports = serial_ports()
    if ser_ports:
        return serial_ports()[0]

def open_port(func):
    def wrapper(self, *args, **kwargs):
        if self.ser is None:
            self.open()
        return func(self, *args, **kwargs)
    return wrapper

class SerialComm(object):
    def __init__(self):
        self.port = None
        self.baudrate = 38400
        self.timeout = 0.1
        self.n_retry = 3
        self.ser = None

    def set(self, port: str = None, baudrate: int = 38400, timeout: float = 0.5):
        self.port = port if port else autodetermine_port()
        self.baudrate = baudrate
        self.timeout = timeout
        self.open()

    def open(self):
        """Connect to serial port"""

        if self.port == None:
            raise Exception('Serial port is not defined')

        if self.ser:
            self.close_port()

        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout
            )
            self.ser.flushInput()
            logger.debug(f"Serial port opened:{self.port}, baud:{self.baudrate}")
            logger.debug(f"Serial port flushed")
        except SerialException as e:
            logger.error(f"Failed to open serial port:{self.port}, error:{e}")
            raise

    def close_port(self):
        """Close serial port"""

        self.ser.close()
        self.ser = None

    @open_port
    def write(self, data: bytes = None):
        """Write bytes to serial port"""

        if not data:
            raise ValueError('No bytes to send')

        logger.debug(f"Data sent: {data}")
        if data:
            try:
                self.ser.write(data)
            except SerialException as e:
                logger.warning(e)
                self.close_port()
                raise

    @open_port
    def read(self, last_char=b'\x83'):
        """Read from serial 1 byte at a time. Stop when last_char is received."""

        frame = b""
        while True:
            try:
                byte = self.ser.read(1)
            except serial.SerialException as e:
                logger.warning(e)
                self.close_port()
                raise
            if byte:
                frame += byte
                if byte == last_char:
                    break
            else:
                break
        logger.debug(f"Data received: {frame}")
        return frame
