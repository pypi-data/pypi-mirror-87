from datetime import datetime
from random import random
from time import sleep
import os

from ziva.const import RV_MASK, WAKE_UP_TIME_TOTAL, REAL_VALUES
from ziva.exceptions import InvalidCommand
from ziva.ziva import Ziva

class ZivaMock(Ziva):
    def __init_(self):
        super().__init__()

    def initialize(self, recv_address: int, rf: bool = True, wake_up_time: int = WAKE_UP_TIME_TOTAL,
                   user_params: list = None):
        mock_file = 'mock_rf.txt' if rf else 'mock_ism.txt'
        self.read_mock_settings(os.path.join(os.path.dirname(os.path.realpath(__file__)), mock_file))
        super().initialize(recv_address=recv_address, rf=rf, wake_up_time=wake_up_time, user_params=user_params)

    def read_mock_settings(self, filepath):
        with open(filepath, 'r', encoding='iso-8859-2') as f:
            lines = f.readlines()
        self.settings = []

        com = None
        for line in lines:
            if '//' in line and len(line.split(':')) == 2:
                com = line.split(':')[1].strip()
            if '//' not in line and len(line.split('=')) == 2:
                name = line.split('=')[0].strip()
                value = line.split('=')[1].strip()
                self.parameters[name] = value
                param = {
                    'name': name,
                    'title': name,
                    'com': com,
                    'value': value,
                    'mode': 'T_STRING'
                }
                self.settings.append(param)

    def write_variable(self, name=None, value=None):
        name, value = str(name), str(value)
        if name in self.parameters:
            self.parameters[name] = value
        else:
            raise NotImplemented

    def read_variable(self, name: str) -> dict:
        """Read variable

        :param name: Name of parameter to read e.g. RECORD_TIME"""
        data_out = {'data':None, 'status':'ok'}
        if name == REAL_VALUES:
            data = []
            if self.rf:
                data.append(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"))
            for i in self.parameters[RV_MASK]:
                if bool(int(i)):
                    data.append(str(round(random()*100, 1)))
            data_out['data'] = data
        else:
            if not name in self.parameters:
                raise InvalidCommand
            data_out['data'] = self.parameters[name]
        return data_out

    def get_memory_status(self) -> dict:
        if self.rf:

            size, free, used = 1000, 500, 500
            self.memory_status = {'size': size, 'free': free, 'used': used,
                                  'used_percentage': round(used / size * 100, 1)}
        else:
            self.memory_status = None
        return self.memory_status

    def start_wake_up_routine(self):
        if self.rf:
            sleep(self.wake_up_time)

    def reset_cpu(self):
        """Reset CPU of device"""
        return True

    def read_params(self, force=True):
        return super().read_params(force=False)

    def set_time(self, timestamp: datetime = datetime.now()):
        return True
