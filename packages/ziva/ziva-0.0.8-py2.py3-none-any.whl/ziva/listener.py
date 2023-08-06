import argparse
from binascii import hexlify

from ziva.serialib import SerialComm, serial_ports, autodetermine_port

parser = argparse.ArgumentParser()
parser.add_argument('-port')

args = parser.parse_args()
port = args.port


def main():
    global port

    if not port:
        if len(serial_ports()) == 0:
            print ('No serial port detected')
            return

        elif len(serial_ports()) > 1:
            print ('Multiple serial ports detected. Please select one:')
            for i, p in enumerate(serial_ports()):
                print (f"{i+1}) {p}")
            port_number = int(input(""))
            port = serial_ports()[port_number - 1].split(' - ')[0]
        else:
            port = autodetermine_port()

    s = SerialComm()
    s.open(port=port, baudrate=38400, timeout=5)
    while True:
        line = s.read()
        print (hexlify(line))

if __name__ == '__main__':
    main()