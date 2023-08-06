""" Communication constants"""


# Structure commands
START_MARKER = '82'
END_MARKER = '83'
START_MARKER_BYTES = b'\x82'
END_MARKER_BYTES = b'\x83'
SERVER_ADDR_BYTES = b'\x00\x00\x00\x00'
EQUALS_SIGN = '{:X}'.format(ord('='))

# Single application commands
VALUE_READ = 'VR'  # Value read
VALUE_WRITE = 'VW'  # Value write
REAL_VALUES = 'RV'  # Value read


# NAME OF PARAMS
IDENT_A = 'IDENT_A'
IDENT_B = 'IDENT_B'
IDENT_C = 'IDENT_C'
ID_0 = 'ID[0]'
RV_MASK = 'RV_MASK'
RV_UNITS = 'RV_UNITS'
RV_NAMES = 'RV_NAMES'
RECORD_TIME = 'RECORD_TIME'
TIME = 'TIME'

WAKE_UP_DEVICE = 'SCWD' # wake up device
DEVICE_SLEEP = 'SCN'
RESET_CPU = 'SRESET'

# Memory operations
OPEN_MEMORY_DIR = 'COFRData0.jda'
MEMORY_START_READING = 'CTFR'
MEMORY_END_READING = 'CCFR'
MEMORY_STATUS = 'FDSX'
FORMAT_DISK = 'FFX0'

# retry
RETRY_NO_ANSWER = 3
RETRY_CRC_ERROR = 10
RETRY_INVALID_ANSWER = 10
RETRY_INVALID_COMMAND = 0

WAKE_UP_TIME_STEP = 30
WAKE_UP_TIME_TOTAL = 30
