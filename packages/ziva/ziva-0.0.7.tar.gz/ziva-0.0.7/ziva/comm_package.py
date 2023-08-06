from binascii import unhexlify

from .const import (
    WAKE_UP_DEVICE,
    START_MARKER_BYTES,
    END_MARKER_BYTES,
    SERVER_ADDR_BYTES
)
from .crc import calculate_crc16
from .exceptions import (
    NoAnswer,
    InvalidAnswer,
    CRCError,
    InvalidCommand,
    DeviceTimeout,
)


def replace_repeating_chars(data: bytes = None, reverse=False) -> bytes:
    """Replace possible repeating chars within communication package
    [0x82] -> [0x84][‘2’]
    [0x83] -> [0x84][‘3’]
    [0x84] -> [0x84][‘4’]

    if reverse:
    [0x82][‘2’] -> [0x82]
    [0x83][‘2’] -> [0x83]
    [0x84][‘2’] -> [0x84]

    :param data: Input communication package (bytes)
    :param reverse: Do a reverse replacing
    :return: Bytes of data
    """
    if reverse:
        data_out = b''
        skip_iter = False
        for i, ch in enumerate(data):
            if skip_iter:
                skip_iter = False
                continue
            if hex(ch) == '0x84':
                if len(data) > (i + 1):
                    skip_iter = True
                    if hex(data[i + 1]) == '0x34':
                        data_out += b'\x84'
                    elif hex(data[i + 1]) == '0x33':
                        data_out += b'\x83'
                    elif hex(data[i + 1]) == '0x32':
                        data_out += b'\x82'
                    else:
                        skip_iter = False
            else:
                data_out += bytes([ch])
    else:
        data_out = data
        data_out = data_out.replace(b'\x84', b'\x844')
        data_out = data_out.replace(b'\x83', b'\x843')
        data_out = data_out.replace(b'\x82', b'\x842')
    return data_out

def data_decompress(data:bytes) -> bytes:
    """Decompress data. Repeating set of chars are compressed into shorter set.
    Set of K equal chars is transformed (K=char, X=number of repeats):
    [F0][X]K ; K=4-239
    [F0][3][K-hi][K-low]X ; K=240-65520

    :data: Bytes to decompress
    :return: Decompress data bytes
     """

    data_out = b''
    i = 0
    while i < len(data):
        ch = data[i]
        if hex(ch) == '0xf0':
            if len(data) > (i + 1):
                n_repeats = data[i + 1]
                if n_repeats == 0:
                    data_out += bytes([ch])
                    i += 2
                    continue
                char = data[i + 2]
                data_out += n_repeats * bytes([char])
                i += 3
                continue
        data_out += bytes([ch])
        i += 1

    return data_out

def define_package(recv_addr: int, app_cmd: str, var_name: str = None, var_val: str = None, counter: int = 0,
                   rf: bool = False) -> bytes:
    """
    Returns string that represent whole communication package. Output string can be directly sent to device.
    Example: read real values from ism (addr 4) "820004FF80000000008101565252563D89C483"

    :param recv_addr: receiver address (e.g. 1000)
    :param app_cmd: application command (e.g. VR - value read)
    :param var_name: variable name (e.g. RV - real values)
    :param var_val: variable value (e.g. `Merilno mest` or `3600`)
    :param rf: RF or not (wifi or wired connection)
    :param counter: package counter (0-255)
    :return: parsed data as string
    """
    if not recv_addr:
        raise ValueError("Receiver address can't be none")

    # Generate receiver address from integer recv_addr
    if rf:
        recv_addr_complete = '{:8X}'.format(recv_addr).replace(' ', '0')
    else:
        recv_addr_1 = '{:2X}'.format(0).replace(' ', '0')
        recv_addr_2 = '{:2X}'.format(recv_addr).replace(' ', '0')
        recv_addr_3 = '{:2X}'.format(255).replace(' ', '0')
        recv_addr_4 = '{:2X}'.format(128).replace(' ', '0')
        recv_addr_complete = recv_addr_1 + recv_addr_2 + recv_addr_3 + recv_addr_4

    # Consts
    recv_addr_complete = unhexlify(recv_addr_complete)
    data_layer = app_cmd
    if var_name:
        data_layer += var_name
    if var_val:
        data_layer += '=' + var_val
    data_layer = data_layer.encode('iso-8859-2')
    if rf and WAKE_UP_DEVICE in app_cmd:
        data_layer += b'\x00'

    # Get hex counter value and 16bit CRC code
    counter_hex = unhexlify('81') + chr(counter).encode('iso-8859-2')
    data_for_crc = recv_addr_complete + SERVER_ADDR_BYTES + counter_hex + data_layer
    crc16 = unhexlify(calculate_crc16(data_for_crc))

    # Combine all data layers
    package = recv_addr_complete + SERVER_ADDR_BYTES + \
              counter_hex + data_layer + crc16
    package = replace_repeating_chars(data=package)
    return START_MARKER_BYTES + package + END_MARKER_BYTES


def data_to_parsed_string(data: bytes):
    """Parse data to list. Separate by comma.
    Example of a raw data: b'\x82\x00\x00\x00\x00\x00\x00\x00\x00\x01@O0.638,0.00,21.67,\to\x83
    """
    data_str = data.decode('iso-8859-2')
    if 'Name' and 'Com' in data_str:
        data_str = list(filter(None, data_str.split(',')))
        data_out = []
        for i, item in enumerate(data_str):
            # If first letter after comma is not in the upper case,
            # merge item with previous item
            if item[0].isupper():
                data_out.append(item)
            else:
                data_out[-1] += ',' + item
        data_str = data_out
    else:
        data_str = list(filter(None, data_str.split(',')))

    return data_str[0] if len(data_str) == 1 else data_str


def validate_data(data: bytes, stream_channel: bool = False) -> dict:
    '''Validate data bytes.
    :param data: input bytes
    :param stream_channel: stream channel uses different status_sign (O, E, OT or OM)
    '''

    if not data:
        raise NoAnswer('No answer from device')
    if len(data) < 14:
        raise InvalidAnswer('Data length is not sufficient')

    start_char = data[0]
    end_char = data[-1]
    data_layer = data[1:-3]
    crc = data[-3:-1]
    crc_ref = unhexlify(calculate_crc16(data_layer))
    if crc != crc_ref or start_char != 130 or end_char != 131:
        raise InvalidAnswer('Invalid answer')

    # Validate data. Possible combinations are:
    # sign @ signals start of message. First letter or first two letters after @ = status:
    # O[value] - okay
    # E[error message] - error
    # OM[data] -> okay, more data
    # OT[data] -> okay, data read complete
    # OE empty dir
    # W[percent] - not yet completed

    at_sign_pos = data_layer.find(b'@')
    if at_sign_pos == -1 or len(data_layer) == at_sign_pos:
        # Error in message if @ is not present or @ is last char in message
        raise InvalidAnswer('Unkown error:', data_layer)

    status_sign_pos = at_sign_pos + 1
    status_sign = chr(data_layer[status_sign_pos])
    if status_sign == 'O' or status_sign == 'W':
        if stream_channel and len(data_layer[status_sign_pos:]) > 1:
            status_sign_additional_letter = chr(data_layer[status_sign_pos + 1])
            if status_sign_additional_letter == 'T' or status_sign_additional_letter == 'M':
                status_sign += status_sign_additional_letter
        data_out = {'status':status_sign, 'data':data_layer[data_layer.find(status_sign.encode()) + len(status_sign):]}
        return data_out

    if status_sign == 'E':
        error_code = chr(data_layer[status_sign_pos + 1])
        error_msg = data_layer[status_sign_pos + 1:]
        if b'implemented' in data_layer:
            raise InvalidCommand('Invalid command')
        elif b'Undefined variable' in data_layer:
            raise InvalidCommand('Undefined variable')
        elif error_code == 'r':
            raise CRCError('Invalid CRC code')
        elif error_code == 'R':
            raise DeviceTimeout
        else:
            raise InvalidAnswer('Unkown error:', error_msg)
    elif status_sign == ' ':
        if b'implemented' in data_layer:
            raise InvalidCommand('Invalid command')
    else:
        raise InvalidAnswer('Status sign is not valid: ', data_layer)
