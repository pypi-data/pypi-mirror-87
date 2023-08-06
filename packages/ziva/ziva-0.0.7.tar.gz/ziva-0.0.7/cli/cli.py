import sys
sys.path.append('..')
sys.path.append('.')
import argparse
import logging
from ziva.serialib import autodetermine_port, serial_ports
from ziva.ziva import Ziva
from ziva.mock import ZivaMock
from ziva.const import VALUE_WRITE, VALUE_READ
from ziva.jda_to_dtv import Jda2dtv

parser = argparse.ArgumentParser()

parser.add_argument('communication_type', choices=["rf", "ism"], help="Communication type")
parser.add_argument('-addr', type=int, help="Device address we wish to communicate with")
parser.add_argument('-port', help="Serial port. Port is automatically set by default")
parser.add_argument('-baud', default=38400, help="Serial port baudrate")
parser.add_argument('-online', default=True, help="Online communication")
parser.add_argument('-loglevel', default='debug', choices=["debug", "info", "warning", "error", "exception"], help="Loglevel")
parser.add_argument('-terminal_mode', action='store_true', help='Go straight to terminal mode')
parser.add_argument('-wake_up_time', default=None, type=int, help='Wake up time for RF devices')
parser.add_argument("--list_ports", action="store_true", help="List COM ports")
parser.add_argument("--mock", action="store_true", help="Use mock object instead of real device")
parser.add_argument("-user_params", nargs='+', help="User parameters")

args = parser.parse_args()
loglevel = args.loglevel.upper()

port = args.port
baud = args.baud
online = args.online
addr = args.addr
comm_type = args.communication_type
rf = True if args.communication_type == 'rf' else False
terminal_mode = args.terminal_mode
list_ports = args.list_ports
mock = args.mock
wake_up_time = args.wake_up_time
user_params = args.user_params

logger = logging.getLogger(__name__)
obj = ZivaMock if mock else Ziva

class ZivaCli(obj):
    def __init__(self):
        super().__init__()

    def terminal_mode(self):
        """Offline terminal mode"""

        app_cmd = input("Application command:").upper() or None
        var_name = input("Variable name:").upper() or None
        var_val = input("Variable value:") or None
        return self.send_receive(app_cmd=app_cmd, var_name=var_name, var_val=var_val)

    def terminal_mode_write_variable(self):
        """Online write terminal mode"""

        var_name = input("Variable name:").upper() or None
        var_val = input("Variable value:") or None
        if not (var_name and var_val):
            raise Exception('Both variable name and variable value must be defined')
        return self.send_receive(app_cmd=VALUE_WRITE, var_name=var_name, var_val=var_val)

    def terminal_mode_read_variable(self):
        """Online write terminal mode"""

        var_name = input("Variable name:").upper() or None
        if not var_name:
            raise Exception('Variable name is not defined')
        return self.read_variable(name=var_name)

def get_input_text():
    input_text = 'Press key for specific task: \n' \
                 'o) Go online \n' \
                 'r) Real values \n' \
                 's) Read settings \n' \
                 'd) Data \n' \
                 'w) Write variable \n' \
                 'f) Read variable \n' \
                 't) Terminal mode \n' \
                 'p) Go to sleep (RF) \n' \
                 'm) Memory status \n' \
                 'rm) Read memory data\n' \
                 'sm) Save memory data\n' \
                 'fm) Format disk\n' \
                 'jd) Convert jda to dtv\n' \
                 'i) Import parameters \n' \
                 'l) Load parameters from file \n' \
                 'e) Export parameters \n' \
                 'dt) Set time to datetime.now() \n' \
                 'c) Reset CPU \n' \
                 'q) Quit\n'
    return input_text

def main():
    global port, baud, online, addr, comm_type, rf, terminal_mode, list_ports

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

    if not addr:
        addr = int(input("Select remote device address:"))

    ziva = ZivaCli()
    ziva.set(port=port, baudrate=baud)
    ziva.initialize(recv_address=addr, rf=rf, wake_up_time=wake_up_time, user_params=user_params)
    while True:
        try:
            if terminal_mode:
                key = 't'
            else:
                key = input(get_input_text())

            if key == 'o':
                try:
                    print (ziva.connect())
                except Exception as e:
                    logger.exception(e)
            elif key == 'r':
                try:
                    print (ziva.get_real_values())
                except Exception as e:
                    logger.exception(e)
            elif key == 's':
                try:
                    params = ziva.read_params()
                    for i in params:
                        print (i)
                except Exception as e:
                    print (e)
            elif key == 'd':
                print (ziva.get_data())
            elif key == 'p':
                print (ziva.goto_sleep())
            elif key == 'c':
                print (ziva.goto_sleep())
            elif key == 'm':
                print (ziva.get_memory_status())
            elif key == 'rm':
                ziva.read_memory_data()
            elif key == 'sm':
                print(ziva.save_memory_data())
            elif key == 'fm':
                print(ziva.format_disk())
            elif key == 'w':
                print(ziva.terminal_mode_write_variable())
            elif key == 'f':
                print(ziva.terminal_mode_read_variable())
            elif key == 'dt':
                ziva.set_time()
            elif key == 'jd':
                filename = input('Enter filename:')
                conv = Jda2dtv()
                conv.load_file(filename)
                conv.write_dJ_file()
                conv.write_dtv_files()
            elif key == 'i':
                ziva.import_params()
            elif key == 'l':
                filepath = input('Enter filepath for loading parameters: \n')
                ziva.load_params(filepath=filepath)
            elif key == 'e':
                filepath = input('Enter filepath for exporting: \n') or None
                try:
                    ziva.export_params(filepath=filepath)
                except Exception as e:
                    logger.exception(e)
            elif key == 't':
                while True:
                    try:
                        print (ziva.terminal_mode())
                    except KeyboardInterrupt:
                        if terminal_mode:
                            exit (0)
                        else:
                            break
                    except Exception as e:
                        print (e)
                        # print (traceback.print_exc(file=sys.stdout))
            elif key == 'q':
                break
        except Exception as e:
            logger.exception(e)
            # print (e)


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=formatter)
    logging.root.setLevel(loglevel)
    main()
