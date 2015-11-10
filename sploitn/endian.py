import struct
def encode(value, num_bytes=4):
    value = value % (2 ** (num_bytes * 8))
    return struct.pack('<L', value)