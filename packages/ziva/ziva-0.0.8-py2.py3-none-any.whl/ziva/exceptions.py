"""Communication exceptions"""


class NotConnectedToSerial(Exception):
    """If connection to serial port was not established"""


class NoAnswer(Exception):
    """There is no answer from a device."""


class InvalidAnswer(Exception):
    """Answer was received but it is now a valid one."""


class CRCError(Exception):
    """CRC Error"""


class InvalidCommand(Exception):
    """Command/Message that was sent is not a valid one"""


class DeviceNotInitialized(Exception):
    """Device is not configured"""


class ParameterError(Exception):
    """One or multiple parameters failed to read/write"""


class DeviceTimeout(Exception):
    """Device timeout"""


class InvalidData(Exception):
    """Invalid data"""
