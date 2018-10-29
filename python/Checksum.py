#!/usr/bin/python3

# checksum from bytes
def checksum(bt):
    if not isinstance(bt, bytes):
        raise TypeError('Expected bytes, got {}'.format(type(bt)))

    tobyte = ord
    if isinstance(bt[0], int):  # Python 3
        tobyte = lambda x: x

    sum = 0
    for i in range(len(bt)):
        sum += tobyte(bt[i]) << (0 if i&1 else 8)

    while (sum >> 16):
        sum = (sum & 0xFFFF) + (sum >> 16)

    return "{:04x}".format((~sum) & 0xFFFF)

# checksum from string
def checksum(data, charset):
    bt = data.encode(charset)
    if not isinstance(bt, bytes):
        raise TypeError('Expected bytes, got {}'.format(type(bt)))

    tobyte = ord
    if isinstance(bt[0], int):  # Python 3
        tobyte = lambda x: x

    sum = 0
    for i in range(len(bt)):
        sum += tobyte(bt[i]) << (0 if i&1 else 8)

    while (sum >> 16):
        sum = (sum & 0xFFFF) + (sum >> 16)

    return "{:04x}".format((~sum) & 0xFFFF)
