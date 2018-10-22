#!/usr/bin/python3

import socket, time, date, os, sys, iplib

def checksum(data):
    if len(data) & 1:
        data = data + b'\0'
    sum = 0
    for i in range(0, len(data), 2):
        sum += ord(data[i]) + (ord(data[i + 1]) << 8)
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)
    return ~sum

class ClientMode:
    def __init__(self, serverIP, serverPort, charset):

        # Initialization of variables
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.charset = charset
        self.tr = "\r\n"
        self.version = "1.7"

        # Construct the client socket
        self.c = socket.socket()
        self.c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.c.connect(self.serverIP, self.serverPort)
        self.c.write("HELLO {}{}".format(self.version, self.tr))

    def clientCommandHandler(self):
        data = self.c.recv(256).decode(self.charset)
        if "\r" not in data:
            self.tr = "\n"
            print("Error, newlines are not CRLF")
            warningHeaders.append("Newlines are not in CRLF form")
        if data == "HELLO {}{}".format(self.version, self.tr):
            print("Hello complete.")
            return "CONTINUE"
        elif "HELLO" in data:
            print("Client Telephone Version Incompatible")
            c.write("GOODBYE{}".format("\r\n").encode(self.charset))
            c.close()
        if data == "SUCCESS{}".format(self.tr):
            c.write("GOODBYE{}".format("\r\n").encode(self.charset))
            return "SUCCESS"
        if data == "GOODBYE".format(self.tr):
            c.close()
            return "TERMINATE"
        if data == "WARN{}".format(self.tr):
            c.write("GOODBYE{}".format("\r\n").encode(self.charset))
            return "WARN"

class ServerMode:
    def __init__(self, listenIP, listenPort, charset):

        # Initialization of variables
        self.listenIP = listenIP
        self.listenPort = listenPort
        self.charset = charset
        self.tr = "\r\n"
        self.version = "1.7"
        self.warningHeaders = []

        # Construct the server socket
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.listenIP, self.listenPort)
        self.s.listen()

    def parseData(self, socket):
        lines = data.split(lr)
        end = -1
        for x in range(0, len(lines)):
            if lines[x] == "."
            end = x
        if end == -1:
            print("Non compliance detected, there is no end of message, indicated by  <CRLF>.<CRLF>")
            warningHeaders.append("No EOM detected")

    def serverCommandHandler(self, socket):
        data = c.recv(256).decode(self.charset)
        if "\r" not in data:
            self.tr = "\n"
            print("Error, newlines are not CRLF")
            warningHeaders.append("Newlines are not in CRLF form")
        if data == "HELLO {}{}".format(self.version, self.tr):
            print("Hello complete.")
            return "CONTINUE"
        elif "HELLO" in data:
            print("Client Telephone Version Incompatible")
            c.write("GOODBYE{}".format("\r\n").encode(self.charset))
            c.close()
        if data == "DATA{}".format(self.tr):
            return "DATA"
        if data == "QUIT".format(self.tr):
            c.write("GOODBYE{}".format("\r\n").encode(self.charset))
            c.close()
            return "TERMINATE"

    def serverInstance(self):
        warningHeaders = []
        c, caddr = self.s.accept()
        c.send("HELLO {}".format(self.version).encode(self.charset))
        # Recieve HELLO version from Client
        run = True
        while run:
            action = self.serverCommandHandler(socket)
            if action == "CONTINUE":
                pass
            if action == "DATA"
                self.parseData(socket)
            if action == "TERMINATE":
                run = False

def printUsage(pname=pname):
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

    if mode:
        # Origination mode
        c = ClientMode(dest, port)
    else:
        # Chain mode



main()
