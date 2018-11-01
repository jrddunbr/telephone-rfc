#!/usr/bin/python3

import socket

print(socket.gethostbyname("google.com"))
try:
    print(socket.gethostbyname("dfsdfjjgelrjglrejtgoijitr.com"))
except:
    print("bad")
print(socket.gethostbyname("128.153.145.3"))
try:
    print(socket.gethostbyname("efjfjljdfs"))
except:
    print("bad")
try:
    print(socket.gethostbyname(""))
except:
    print("bad")

d = """


def checksum(data):
    if type(data) != type(b'\0'):
        print("[CRITICAL BUG] NON ENCODED DATA PASSED TO CHECKSUM FUNCTION")
    if len(data) & 1:
        data = data + b'\0'
    sum = 0
    for i in range(0, len(data), 2):
        sum += data[i] + (data[i + 1]) << 8
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)
    return "{:04x}".format((~sum) & 0xFFFF)

print(checksum("DOOT!".encode("ascii")))
"""
