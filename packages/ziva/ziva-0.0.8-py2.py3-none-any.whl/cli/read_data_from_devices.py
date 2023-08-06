import sys
import argparse
import logging
from time import sleep
sys.path.append('..')
sys.path.append('.')
from ziva.exceptions import NoAnswer
from ziva.ziva import Ziva

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-addrs', type=int, nargs='+', help="Device address we wish to communicate with")
parser.add_argument('-port', help="Serial port. Port is automatically set by default")
parser.add_argument('-baud', default=38400, help="Serial port baudrate")
parser.add_argument('-loglevel', default='debug', choices=["debug", "info", "warning", "error", "exception"],
                    help="Loglevel")
parser.add_argument('-wake_up_time', default=None, type=int, help='Wake up time for RF devices')
parser.add_argument('-dir', default='', help="Directory for data")
parser.add_argument('-retry', default=1, type=int, help="Retry")
parser.add_argument('-directory', default='', help="Directory to store data in")
args = parser.parse_args()


def main(port=None, baud=None, addrs=None, wake_up_time=None, directory=None, retry=None):
    ziva = Ziva()
    ziva.set(port=port, baudrate=baud)
    completed = []
    failed_connect = []
    failed_disconnect = []
    failed_data = []
    for addr in addrs:
        sleep(2)
        try:
            ziva.initialize(recv_address=addr, rf=True, wake_up_time=wake_up_time)
            for i in range(retry):
                try:
                    print(f'Connecting to device {addr}, retry={i}')
                    ziva.connect()
                    break
                except NoAnswer:
                    sleep(1)
                    if i == retry - 1:
                        failed_connect.append(addr)
                        raise

            for i in range(retry):
                try:
                    print(f'Reading data from device {addr}, retry={i}')
                    ziva.read_memory_data()
                    ziva.save_memory_data(directory=directory)
                    completed.append(addr)
                    break
                except Exception as e:
                    print (e)
                    if i == retry - 1:
                        failed_data.append(addr)
                    sleep(1)
            try:
                ziva.disconnect(deinit=False)
            except Exception:
                failed_disconnect.append(addr)
        except Exception:
            pass

    print ('\n\n')
    print(f'Completed: {completed}')
    print(f'Failed connected: {failed_connect}')
    print(f'Failed disconnected: {failed_disconnect}')
    print(f'Failed data: {failed_data}')


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=formatter)
    logging.root.setLevel(args.loglevel.upper())
    main(port=args.port, baud=args.baud, addrs=args.addrs,
         wake_up_time=args.wake_up_time, directory=args.directory, retry=args.retry)
