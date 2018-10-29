#!/usr/bin/python3

from DataHandler import DataHandler
import Checksum

h = DataHandler("utf-8", "\n")

f = open("test.txt")
data = "".join(f.readlines())
f.close()

#print(data)

print(h.parseIncoming(data))
