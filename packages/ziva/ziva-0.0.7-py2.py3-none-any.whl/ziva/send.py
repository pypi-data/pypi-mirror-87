import argparse
import logging
from binascii import unhexlify

from ziva.serialib import SerialComm, serial_ports, autodetermine_port

parser = argparse.ArgumentParser()
parser.add_argument('-port')
parser.add_argument('-loglevel', default='debug', choices=["debug", "info", "warning", "error", "exception"], help="Loglevel")

args = parser.parse_args()
loglevel = args.loglevel.upper()
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
    s.open(port=port, baudrate=38400, timeout=0.5)
    data = eval(input('Enter data to send [hex string]:'))
    print ('this is data', data)
    data = data.replace(' ', '')
    data = unhexlify(data)
    s.write(data=data)
    answer = s.read()
    print ('Received data: ', answer)

if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=formatter)
    logging.root.setLevel(loglevel)
    main()