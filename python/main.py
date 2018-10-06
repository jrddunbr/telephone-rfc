#!/usr/bin/python3

import socket, time, date, os, sys, iplib

VERSION = "1.7"

def buildPacket():
    pass

class ClientMode:
    def __init__(self):
        pass

class ServerMode:
    def __init__(self, listenIP, listenPort, charset):
        self.listenIP = listenIP
        self.listenPort = listenPort
        self.charset = charset
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(self.listenIP, self.listenPort)
        s.listen()

    def step(self):
        warningHeaders = []
        c, caddr = s.accept()
        c.send("HELLO {}".format(VERSION).encode(self.charset))
        data = c.recv(1024).decode(self.charset)
        if not data:
            c.send("QUIT".encode(self.charset))
            c.close()
            return
        if data.split("\n")[0].strip() != "HELLO {}".format(VERSION):
            c.send("QUIT".encode(self.charset))
            c.close()
            return
        data = c.recv(1024).decode(self.charset)
        if not data:
            c.send("QUIT".encode(self.charset))
            c.close()
            return
        lr = "\r\n"
        if not "\r" in data:
            lr = "\n"
            print("Non compliance detected, line feeds are not proper CRLF characters")
            warningHeaders.append("CRLF is not properly enumerated. Using LF only.")
        lines = data.split(lr)
        end = -1
        for x in range(0, len(lines)):
            if lines[x] == "."
            end = x
        if end == -1:
            print("Non compliance detected, there is no end of message, indicated by  <CRLF>.<CRLF>")
            warningHeaders.append("No end of message detected")
        ehdr = -1
        for x in range(0, len(end)):
            if lines[x] == ""
            ehdr = x
        if ehdr == -1:
            print("Non compliance detected, there is no header seperation.")
            warningHeaders.append("Error, headers not properly enumerated.")
        






def printUsage(pname = pname):
    print("Usage:\n")
    if pname != None:
        pname = ""
    print("{} <dest> [mode] [charset] [source]\n".format(pname))
    print("Where:")
    print("* dest is the destination IP address for the next hop")
    print("* source is the source IP from the previous hop")
    print("* mode is the mode that the program operates in:")
    print("\t* 0, o, originator, init, or start: originates the first packet")
    print("\t* 1, or chain: (default) allows packets incoming and repeats to next hop")
    print("* charset is either ascii or utf8")
    sys.exit(0)

def main():
    dest = ""
    source = "0.0.0.0" # default source address - any address
    mode = False # False is not originiate, ie, chain mode
    charset = "utf-8"
    if len(sys.args) == 2:
        # dest
        dest = sys.args[1]
    elif len(sys.args) == 3:
        # dest, mode
        dest = sys.args[1]
        ms = sys.args[2].lower().strip()
        mode = ms == "0" or ms == "o" or or ms == "originator" or ms == "init" or ms == "start"
    elif len(sys.args) == 4:
    # dest, mode, source
        dest = sys.args[1]
        ms = sys.args[2].lower().strip()
        mode = ms == "0" or ms == "o" or or ms == "originator" or ms == "init" or ms == "start"
        charset = sys.args[3]
    elif len(sys.args) == 5:
    # dest, mode, source
        dest = sys.args[1]
        ms = sys.args[2].lower().strip()
        mode = ms == "0" or ms == "o" or or ms == "originator" or ms == "init" or ms == "start"
        charset = sys.args[3]
        source = sys.args[4]
    else:
        # error, do the usage dialog
        printUsage()

    if not iplib.checkIPv4(dest):
        print("Sorry, but {} is not a valid IPv4 address".format(dest))
        sys.exit(1)

    if not iplib.checkIPv4(source):
        print("Sorry, but {} is not a valid IPv4 address".format(source))
        sys.exit(1)

    if charset not in ["utf-8", "ascii"]:
        print("Invalid Charset")
        sys.exit(1)

main()
