#!/usr/bin/python3

from DataHandler import DataHandler
import Checksum

nm = input("Filename: ")

f = open(nm)
data = "".join(f.readlines())
f.close()

le = "\r\n"

if not "\r" in data:
    le = "\n"

h = DataHandler("utf-8", le)

notes = h.parseIncoming(data)

h.getNewHopNum()

print(h.createOutgoing("10.0.0.1", 2343, "10.4.5.2", 3245, h.full_message))
