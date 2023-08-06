import logging

import argparse
from ziva.serialib import serial_ports, SerialComm

parser = argparse.ArgumentParser()

parser.add_argument('-port', help="Serial port")
parser.add_argument('-baud', default=38400, help="Serial port baudrate")
parser.add_argument('-loglevel', default='debug', choices=["debug", "info", "warning", "error", "exception"], help="Loglevel")

args = parser.parse_args()
port = args.port
loglevel = args.loglevel.upper()
baud = args.baud


class Router(SerialComm):
    def __init__(self, port:str, baudrate:int, timeout=5):
        super().__init__()
        self.open(port=port, baudrate=baudrate, timeout=timeout)

    def send_okay(self):
        return self.write(data=b'\x82\x00\x00\x00\x00\x00\x00\x00\x00\x01@O\xf4!\x83')

    def send_data_part(self):
        return self.write(b'\x82\x00\x00\x00\x00\x00\x00\x00\x00A@OM$HEADER START\r\nFILE_TYPE=2\r\nIDENT_A=RFT90019\r\nIDENT_B=DMS 2AAA 160120\r\nIDENT_C=MEMO-RFT90019 v1.1\r\nCH_BITS=24,8,\r\nCHAN_UBPOL=\xf0\x08U\r\nCHAN_SIDIF=\xf0\x04S\xf0\x04D\r\nCHAN_BUFFER=\xf0\x04-\xf0\x04B\r\nCHAN_RANGE=55\xf0\x067\r\nCHAN_FIL=32,32,32,32,84,84,84,16,\r\nMAX_NO_RVS=4\r\n\x81\x8a\x83')

    def respond_to_cofr(self):
        return self.write(b'\x82\x00\x00\x00\x00\x00\x00\x00\x00A@O65533$\t\x83')

    def respond_to_fdsx(self):
        return self.write(b'\x82\x00\x00\x00\x00\x00\x00\x00\x00A@O8139,3112,5027,0@T\x83')

    def listen_loop(self):
        while True:
            request = self.read()
            data = ''.join(chr(i) for i in request)
            print (data)
            if 'CTFR' in data:
                self.send_data_part()
            elif 'COFR' in data:
                self.respond_to_cofr()
            elif 'FDSX' in data:
                self.respond_to_fdsx()
            else:
                self.send_okay()


def main():
    global port, baud
    if not port:
        if len(serial_ports()) == 0:
            print('No serial port detected')
            return

        elif len(serial_ports()) > 1:
            print('Multiple serial ports detected. Please select one:')
            for i, p in enumerate(serial_ports()):
                print(f"{i + 1}) {p}")
            port_number = int(input(""))
            port = serial_ports()[port_number - 1].split(' - ')[0]

    timeout = 10
    router = Router(port=port, baudrate=baud, timeout=timeout)
    router.listen_loop()

if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=formatter)
    logging.root.setLevel(loglevel)
    main()



