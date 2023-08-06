import logging
import os
import re
from itertools import compress
from time import sleep, time
from datetime import datetime

from serial import SerialException

from ziva.jda_to_dtv import Jda2dtv
from .comm_package import validate_data, define_package, data_to_parsed_string, replace_repeating_chars, data_decompress
from .serialib import SerialComm
from .const import *
from .exceptions import (
    NoAnswer, InvalidAnswer,
    InvalidCommand,
    CRCError,
    DeviceNotInitialized,
    ParameterError,
    DeviceTimeout,
    InvalidData
)

logger = logging.getLogger(__name__)


class Ziva(SerialComm):
    def __init__(self):
        super().__init__()
        # Serial port
        self.port = None
        self.baudrate = 38400
        self.timeout = 1
        self.package_counter = 64

        self.recv_address = None
        self.rf = None

        # Real values (actual values from device)
        self.rv_units = []
        self.rv_names = []
        self.real_values = []

        # info values, user values and memory status
        # Latest data combines all of the above with last
        self.info_values = {}
        self.user_values = {}
        self.memory_status = None
        self.data = {
            'real_values': self.real_values,
            'info_params': self.info_values,
            'user_params': self.user_values,
            'memory_status': self.memory_status,
        }

        self.parameters = {}  # dict of all parameters that are read
        self.settings = []

        self.memory_data = []

        # Application commands for communication
        self.real_values_params = [RV_MASK, RV_UNITS, RV_NAMES]
        self.info_params = [IDENT_A, IDENT_B, IDENT_C]
        self.user_params = []

        # Information for reading memory data
        self.total_data_len = 0
        self.total_data_read = 0
        self.read_memory_progress = 0

    def __update_param(self, name, value):
        self.parameters[name] = value
        # also update in settings
        item = [i for i in self.settings if i['name'] == name]
        if item:
            item[0]['value'] = value

    def __increment_counter(self):
        """Counter. Increment counter after every sent packet"""

        if self.package_counter == 127:
            self.package_counter = 64
        else:
            self.package_counter += 1

    def __define_package(self, app_cmd: str = None, var_name: str = None, var_val: str = None):
        """Define package
        :param app_cmd: Application command (VR (Value read), VW (Value write),...)
        :param var_name: Variable name  (RV, IDENT_A, IDENT_B,..)
        :param var_val: Variable value (string that can represent anything)
        """

        package = define_package(
            recv_addr=self.recv_address,
            app_cmd=app_cmd,
            var_name=var_name,
            var_val=var_val,
            counter=self.package_counter,
            rf=self.rf
        )
        return package

    def initialize(self, recv_address: int, rf: bool = True, wake_up_time: int = WAKE_UP_TIME_TOTAL,
                   user_params: list = None):
        """
        Set device. Call this on start of the communication.

        :param recv_address: receiver address (eg 1 for ISM or 1019 for RF)
        :param rf: RF or ISM
        :user_params : Additional user params that are called when connecting to device
        """

        self.recv_address = recv_address
        self.rf = rf
        self.user_params = []
        self.user_values = {}
        self.wake_up_time = wake_up_time if wake_up_time else WAKE_UP_TIME_TOTAL
        if self.rf:
            self.user_params.append(RECORD_TIME)
            self.timeout = 2
        if user_params:
            self.user_params += user_params

    def deinitialize(self):
        """Deinitialize device."""

        self.__init__()

    def read_variable(self, name: str) -> dict:
        """Read variable

        :param name: Name of parameter to read e.g. RECORD_TIME"""

        if name is None:
            raise ValueError('Name of the variable is not defined')
        data = self.send_receive(app_cmd=VALUE_READ, var_name=name)
        self.parameters[name] = data['data']
        return data

    def write_variable(self, name=None, value=None) -> dict:
        """Write variable

        :param name: Name of parameter to write e.g. RECORD_TIME
        :param value: Value to write e.g. 60
        :return ??
        """

        if name is None or value is None:
            raise ValueError('Name or value of the variable is not defined')
        name, value = str(name), str(value)
        data = self.send_receive(app_cmd=VALUE_WRITE, var_name=name, var_val=value)
        self.__update_param(name=name, value=value)
        return data

    def send_receive(self, app_cmd: str, var_name: str = None, var_val: str = None, retry_limit: int = 5,
                     timeout: float = 1, stream_channel: bool = False, parse_to_str: bool = True) -> dict:
        """Sent package and receive answer."""

        if not self.recv_address:
            raise DeviceNotInitialized('Device is not initialized')

        if self.ser is not None:
            # Update timeout for serial if it changes
            if timeout != self.ser.timeout:
                self.ser.timeout = timeout

        for error_count in range(retry_limit):
            package = self.__define_package(
                app_cmd=app_cmd,
                var_name=var_name,
                var_val=var_val,
            )
            try:
                self.write(data=package)
                data = self.read(last_char=END_MARKER_BYTES)
            except SerialException as e:
                logger.warning(e)
                raise
            try:
                replaced_data = replace_repeating_chars(data, reverse=True)
                validated_data = validate_data(replaced_data, stream_channel=stream_channel)
                if parse_to_str:
                    validated_data['data'] = data_to_parsed_string(data=validated_data['data'])
                self.__increment_counter()
            except CRCError as e:
                logger.warning(e)
                self.__increment_counter()
                if retry_limit == error_count + 1:
                    logger.error(e)
                    raise
            except InvalidAnswer as e:
                logger.warning(e)
                self.__increment_counter()
                if stream_channel:
                    # After InvalidAnswer is raised we cannot stream data anymore because data packages are invalid
                    raise InvalidData('Invalid data from device')
                if retry_limit == error_count + 1:
                    logger.error(e)
                    raise
            except (NoAnswer, DeviceTimeout) as e:
                logger.warning(e)
                if retry_limit == error_count + 1:
                    logger.error(e)
                    self.__increment_counter()
                    raise
            except (InvalidCommand, Exception) as e:
                self.__increment_counter()
                logger.warning(e)
                raise
            else:
                return validated_data

    def get_data(self) -> dict:
        """ Get latest data from device and update parameters if they were changed

        :return: dictionary with latest data
        """

        self.data['real_values'] = self.get_real_values()
        self.data['info_params'] = self.get_params(params=self.info_params)
        self.data['user_params'] = self.get_params(params=self.user_params)
        self.data['memory_status'] = self.memory_status

        return self.data

    def get_params(self, params: list = None):
        for param in params:
            if param not in self.parameters:
                value = None
                try:
                    value = self.read_variable(name=param)['data']
                except (InvalidCommand, InvalidAnswer):
                    # Save None to param if an invalid command is executed
                    pass
                except Exception:
                    raise
                self.__update_param(name=param, value=value)
        return {k: v for (k, v) in self.parameters.items() if k in params}

    def get_real_values(self) -> list:
        """ Read real values from device
        Possible output from real values variable:
        - ISM: '7005968.000','0.00','-83.94'
        - RF: '29/08/2020 18:39:47','25.740','3.42'
        """

        rv_mask = [bool(int(i)) for i in self.get_params([RV_MASK])[RV_MASK]]
        rv_units = self.get_params([RV_UNITS])[RV_UNITS].split(';')
        rv_names = self.get_params([RV_NAMES])[RV_NAMES].split(';')
        rv_units = list(compress(rv_units, rv_mask))
        rv_names = list(compress(rv_names, rv_mask))

        # Read real values
        real_values = self.read_variable(name=REAL_VALUES)['data']
        self.real_values = []

        # First real value can be timestamp
        try:
            datetime.strptime(real_values[0], "%d/%m/%Y %H:%M:%S")
            self.real_values.append({'channel': 'Timestamp', 'value': real_values[0], 'unit': None})
            real_values.pop(0)
        except ValueError:
            pass

        for i, val in enumerate(real_values):
            try:
                meas = {
                    'channel': rv_names[i] if len(rv_names) > i else None,
                    'value': val,
                    'unit': rv_units[i] if len(rv_units) > i else None
                }
                self.real_values.append(meas)
            except IndexError as e:
                logger.exception(e)
        return self.real_values

    def get_time(self):
        """Get time from device"""

        return self.read_variable(name=TIME)

    def set_time(self, timestamp: datetime = datetime.now()):
        """Set time of device

        :param timestamp: timestamp to set; if None datetime.now() is used
        :type timestamp: datetime
        """

        if timestamp is None:
            timestamp = datetime.now()
        if type(timestamp) == str:
            try:
                timestamp = datetime.strptime(timestamp.replace(microsecond=0), '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                # print (e)
                raise ValueError('Wrong time format')
        timestamp = str(timestamp.replace(microsecond=0))
        return self.write_variable(name=TIME, value=timestamp)

    def get_memory_status(self) -> dict:
        """Read memory status"""

        if self.rf:
            try:
                data = self.send_receive(app_cmd=MEMORY_STATUS)['data']
                size, free, used = int(data[0]), int(data[1]), int(data[2])
                self.memory_status = {'size': size, 'free': free, 'used': used,
                                      'used_percentage': round(used / size * 100, 1)}
            except InvalidCommand:
                self.memory_status = {'error': True}
        else:
            self.memory_status = None
        return self.memory_status

    def read_params(self, force=True):
        """Read parameters from device"""

        if self.settings and not force:
            return self.settings
        data = []
        error_count = 0
        max_error_count = 5
        for i in range(500):
            var_name = f'PAR[{i}]'
            try:
                params = self.send_receive(app_cmd=VALUE_READ, var_name=var_name)['data']
                if params == 'End':
                    break
                elif len(params) > 0:
                    params_dict = {}
                    for par in params:
                        if '=' in par:
                            params_dict[par.split('=')[0].lower()] = par.split('=')[1]
                        else:
                            params_dict[par.lower()] = True
                    value = self.read_variable(name=params_dict['name'])['data']
                    params_dict['value'] = value

                    # Extract choices
                    # {'mode': 'T_LIST', 'i0': '0 Enable', 'i1': '1 Disable'}
                    if 'mode' in params_dict:
                        mode = params_dict['mode']
                        if mode == 'T_LIST':
                            choices = []
                            for x in range(0, 50):
                                if f'i{x}' in params_dict:
                                    value = params_dict[f'i{x}'].split(' ')[0]
                                    title = params_dict[f'i{x}'].split(' ')[1]
                                    choices.append({'value': value, 'title': title})
                                else:
                                    break
                            params_dict['choices'] = choices
                    data.append(params_dict)
            except Exception as e:
                logger.warning(f'Cant read param {var_name}, e:{e}')
                error_count += 1
                if error_count == max_error_count:
                    break
                else:
                    continue
        logger.info(f'Settings parameters read, count:{len(data)}')
        self.settings = data
        return data

    def read_memory_data(self) -> bytes:
        """Read data from memory of device and save to memory_data

        :return: Bytes of read data
        """

        self.total_data_read = 0
        self.read_memory_progress = 0
        self.total_data_len = int(self.send_receive(app_cmd=OPEN_MEMORY_DIR)['data'])
        data_out = b''
        while True:
            data = self.send_receive(app_cmd=MEMORY_START_READING, parse_to_str=False,
                                     stream_channel=True, timeout=2, retry_limit=7)
            data['data'] = data_decompress(data['data'])
            self.__update_read_memory_progress(data['data'])
            data_out += data['data']
            if data['status'] == 'OT':
                self.send_receive(app_cmd=MEMORY_END_READING)
                break

        if data_out:
            header, body = data_out.split(b'$HEADER END\r\n')
            header = header.replace(b'\r\n', b'\n') + b'$HEADER END\n'
            self.memory_data = header + body
            return self.memory_data

    def save_memory_data(self, directory='', dtv=True) -> str:
        """Read data from memory of device and save to files.

        :param directory: directory for saving files
        :param dtv: save to dtv format

        Return filepath of created dJ file
        """

        ts = datetime.strftime(datetime.now(), "%d%m%Y_%H%M")
        filename = f"{self.get_params(['IDENT_A'])['IDENT_A']}_{ts}.jda"
        # Replace all chars that are not allow for path (<>;?\/|*) with empty string
        replacements = ['<', '>', ':', '?', '\\', '*', '|', '/']
        for i in replacements:
            filename = filename.replace(i, '')
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(self.memory_data)
        conv = Jda2dtv()
        conv.load_file(filepath)
        if dtv:
            conv.write_dtv_files()
        conv.write_dJ_file()
        return filepath.replace('.jda', '.dJ')

    def format_disk(self):
        """Format disk"""

        return self.send_receive(app_cmd=FORMAT_DISK, timeout=5)

    def export_params(self, filepath: str = 'settings.txt'):
        """Save params to filepath"""

        data = self.read_params(force=False)
        data_write = []
        for i, param in enumerate(data):
            # print (param)
            comment = param['com']
            value = param['value']
            name = param['name']
            data_write.append(f'// Par {i}: {comment}\n')
            data_write.append(f'{name}={value}\n')
        with open(filepath, 'w', encoding='iso-8859-2') as f:
            f.writelines(data_write)
        logger.info(f'Parameters exported: {len(data)}')

    def import_params(self):
        """Import parameters from self.settings to device."""

        if not self.settings:
            raise ParameterError('Zero parameters to import')

        data = self.settings
        failed = []
        for item in data:
            name = item['name']
            value = item['value']
            try:
                self.write_variable(name=name, value=value)
            except Exception as e:
                logger.error(f'Failed to write param {name}, e:{e}')
                failed.append((name, value))

        logger.info(
            f"Parameters imported:{len(data) - len(failed)}{', error:{}'.format(len(failed)) if failed else ''}")
        if failed:
            raise ParameterError(f'Parameters failed to import {[i[0] for i in failed]}')

    def load_params(self, filepath: str) -> list:
        """Load parameters from file into settings variable. Params are loaded not
        actually imported to device. Call import_params for importing this params into device

        :param filepath: Filepath of file with parameters.
        """

        if filepath is None or not os.path.exists(filepath):
            raise FileNotFoundError('File does not exists')

        with open(filepath, encoding='iso-8859-2') as f:
            lines = f.readlines()

        data = []
        for i, line in enumerate(lines):
            if '//' in line:
                try:
                    par = line.split('Par ')[1].split(':')[0]
                    com = "".join(line.split(': ')[1]).strip()
                    line = lines[i + 1]
                    if not re.search('//', line) and re.search('=', line):
                        name = line.split('=')[0].strip()
                        value = line.split('=')[1].strip()
                        data.append({'param':par, 'name': name, 'value': value, 'com': com})
                except IndexError as e:
                    logger.exception(e)
                    pass

        failed = []
        if self.settings:
            for item in data:
                # Replace values with the ones from file
                item_settings = [i for i in self.settings if i['name'] == item['name']]
                if item_settings:
                    item_settings[0]['value'] = item['value']
                else:
                    failed.append(item['name'])
                    logger.error(f'Failed to load param {item["name"]}')
        else:
            self.settings = data
        if failed:
            raise ParameterError(f'Parameters failed to import {[i for i in failed]}')
        return self.settings

    def reset_rf_device(self):
        # !!! Not done
        pass

    def reset_cpu(self):
        """Reset CPU of device"""

        return self.send_receive(app_cmd=RESET_CPU)

    def goto_sleep(self):
        """Send RF device to sleep"""

        return self.send_receive(app_cmd=DEVICE_SLEEP)

    def start_wake_up_routine(self):
        """Start wake up procedure for RF devices"""

        if self.rf:
            start = time()
            app_cmd = f"{WAKE_UP_DEVICE}{self.recv_address},{self.wake_up_time}"
            try:
                self.send_receive(app_cmd=app_cmd, retry_limit=3, timeout=0.1)
                sleep(self.wake_up_time)
            except NoAnswer:
                raise NoAnswer('USB router is not working properly')
            wake_time = round(time() - start, 1)
            logger.info(f'Device woke up in {wake_time} seconds')

    def connect(self) -> dict:
        """Connect to device (Online mode). If remote device is RF start wake_up procedure."""
        if not self.recv_address:
            raise DeviceNotInitialized('Device is not initialized')

        self.start_wake_up_routine()
        self.get_memory_status()
        data = self.get_data()
        return data

    def disconnect(self, deinit: bool = True):
        """Disconnect from device"""
        if self.rf:
            self.reset_cpu()
        if deinit:
            self.deinitialize()

    def __update_read_memory_progress(self, read_data:bytes):
        """ Update progress in percentage for reading data from device memory

        :param: Read data (one package)
        """
        self.total_data_read += len(read_data)
        self.read_memory_progress = round((self.total_data_read) / self.total_data_len * 100, 1)


if __name__ == '__main__':
    z = Ziva()
