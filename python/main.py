#!/usr/bin/python3

import socket, time, datetime, os, sys, iplib, string, random, platform

DBG = True

def checksum(data):
    if len(data) & 1:
        data = data + b'\0'
    sum = 0
    for i in range(0, len(data), 2):
        sum += ord(data[i]) + (ord(data[i + 1]) << 8)
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)
    return (~sum) & 0xFFFF

def mkRandNum(size):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))

class HeaderHandler:
    def __init__(self):
        self.raw_headers = ""
        self.hop = {}

    def feedIncomingHeaders(self, headerString):
        self.raw_headers = headerString
        self.lraw_headers = self.raw_headers.lower()

    def getHighestHopNum(self):
        if self.lraw_headers == "":
            return 0
        else:
            hops = [x for x in self.lraw_headers.split("\n") if "hop" in x]
            print(hops)
            try:
                nums = [x for x in int(hops.split(":",1)[1].strip())]
                # get biggest hop number
                b = 0
                for num in nums:
                    if num > b:
                        b = num
                return num + 1 # because we're the next hop
            except:
                return 30 # hardcoded size because I have hit an error, and likely
                # that there are not more than 30 people in class with programs.
                # I can't imagine what happens when the next program tries to parse
                # the headers if there's a duplicate...

    def getMessageId(self):
        if self.lraw_headers == "":
            return 0
        else:
            return [x for x in self.lraw_headers.split("\n") if "messageid" in x][0].split(":",1)[1].strip()

    def generateOutgoingHeaders(self, dest, destp, src, srcp, msg):
        outputHeaders = ""
        if self.raw_headers == "":
            # generate clean headers
            self.hop[0] = {}
            self.hop[0]["Hop"] = str(0)
            self.hop[0]["MessageId"] = str(mkRandNum(8))
            self.hop[0]["FromNetworkAddress"] = "{}:{}".format(src, srcp)
            self.hop[0]["ToNetworkAddress"] = "{}:{}".format(dest, destp)
            self.hop[0]["System"] = "{} {} {}".format(platform.system(), platform.machine(), platform.release())
            self.hop[0]["Program"] = "{}/{}".format("Python", platform.python_version())
            self.hop[0]["Author"] = "Jared Dunbar"
            tm = datetime.datetime.now()
            self.hop[0]["SendingTimestamp"] = "{}:{}:{}:{}".format(tm.hour, tm.minute, tm.second, int(tm.microsecond / 100))
            self.hop[0]["MessageChecksum"] = checksum(msg)
            return str(self.hop[0])
        else:
            # generate new headers on top of the existing headers

            d = """
        headers = outputHeaders

Hop: 1
MessageId: 3456
FromNetworkAddress: 192.168.0.12:9879
ToNetworkAddress: 192.168.0.4:8888
System: WINDOWS/XP
Program: JAVA/JAVAC
Author: Frodo Baggins
SendingTimestamp: 17:00:00:000
MessageChecksum: 432F
HeadersChecksum: A350
Hop: 0
MessageId: 3456
NetworkFromAddress: 192.168.0.1:34953
NetworkToaddress: 192.168.0.12:8888
System: LINIX/DEBIAN/R3.0
Program: C++/GCC
Author: Alex, J./Jacky Elton/David Wang
SendingTimestamp: 16:59:59:009
MessageChecksum: 423F
HeadersChecksum: 6F38
"""

class ClientMode:
    def __init__(self, serverIP, serverPort, charset):

        # Initialization of variables
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.charset = charset
        self.tr = "\r\n"
        self.version = "1.7"
        self.warningHeaders = []

        # Construct the client socket
        self.c = socket.socket()
        self.c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.c.connect((self.serverIP, self.serverPort))

    def clientCommandHandler(self):
        data = self.c.recv(256).decode(self.charset)
        if "\r" not in data:
            self.tr = "\n"
            print("[err] Newlines are not CRLF")
            self.warningHeaders.append("Newlines are not in CRLF form")
        if data == "HELLO {}{}".format(self.version, self.tr):
            self.c.send("HELLO {}\r\n".format(self.version).encode(self.charset))
            if DBG: print("[dbg] Hello complete.")
            return "CONTINUE"
        elif "HELLO" in data:
            print("[err] Client Telephone Version Incompatible")
            self.c.send("GOODBYE{}\r\n".format("\r\n").encode(self.charset))
            self.c.close()
        if data == "SUCCESS{}".format(self.tr):
            self.c.send("GOODBYE{}\r\n".format("\r\n").encode(self.charset))
            return "SUCCESS"
        if data == "GOODBYE".format(self.tr):
            self.c.close()
            return "TERMINATE"
        if data == "WARN{}".format(self.tr):
            self.c.send("GOODBYE{}\r\n".format("\r\n").encode(self.charset))
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
            if lines[x] == ".":
                end = x
        if end == -1:
            print("[err] Non compliance detected, there is no end of message, indicated by  <CRLF>.<CRLF>")
            self.warningHeaders.append("No EOM detected")

    def serverCommandHandler(self, socket):
        if "\r" not in data:
            self.tr = "\n"
            print("[err] Newlines are not CRLF")
            self.warningHeaders.append("Newlines are not in CRLF form")
        if data == "HELLO {}{}".format(self.version, self.tr):
            if DBG: print("[dbg] Hello complete.")
            return "CONTINUE"
        elif "HELLO" in data:
            print("[err] Client Telephone Version Incompatible")
            c.send("GOODBYE{}\r\n".format("\r\n").encode(self.charset))
            c.close()
        if data == "DATA{}".format(self.tr):
            return "DATA"
        if data == "QUIT".format(self.tr):
            c.send("GOODBYE{}\r\n".format("\r\n").encode(self.charset))
            c.close()
            return "TERMINATE"

    def serverInstance(self):
        warningHeaders = []
        c, caddr = self.s.accept()
        c.send("HELLO {}\r\n".format(self.version).encode(self.charset))
        # Recieve HELLO version from Client
        run = True
        while run:
            action = self.serverCommandHandler(socket)
            if action == "CONTINUE":
                pass
            if action == "DATA":
                self.parseData(socket)
            if action == "TERMINATE":
                run = False

def printUsage():
    print("Usage:\n")
    pname = "python3 main.py"
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
    defport = 32409
    mode = False # False is not originiate, ie, chain mode
    charset = "ascii"
    if len(sys.argv) == 2:
        # dest
        dest = sys.argv[1]
    elif len(sys.argv) == 3:
        # dest, mode
        dest = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms == "init") or (ms == "start")
    elif len(sys.argv) == 4:
    # dest, mode, source
        dest = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms == "init") or (ms == "start")
        charset = sys.argv[3]
    elif len(sys.argv) == 5:
    # dest, mode, source
        dest = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms == "init") or (ms == "start")
        charset = sys.argv[3]
        source = sys.argv[4]
    else:
        # error, do the usage dialog
        printUsage()

    if not iplib.checkIPv4maybePort(dest):
        print("[err] Sorry, but {} is not a valid IPv4 address".format(dest))
        sys.exit(1)

    if not iplib.checkIPv4maybePort(source):
        print("[err] Sorry, but {} is not a valid IPv4 address".format(source))
        sys.exit(1)

    if charset not in ["utf-8", "ascii"]:
        print("[err] Invalid Charset")
        sys.exit(1)

    if DBG: print("[dbg] stuff looks good. starting")
    print("dest: {}\nsource: {}\ncharset: {}\nmode: {}".format(dest, source, charset, mode))

    if mode:
        # Origination mode
        if DBG: print("[dbg] Entering ORIGIN mode")
        message = input("Input message:\n")
        print("=======\nMessage:")
        print(message)
        if iplib.hasPort(dest):
            dest = dest.split(":",1)[0]
            port = int(dest.split(":",1)[1])
        else:
            if DBG: print("[dbg] Using default port of {}".format(defport))
            port = defport
        c = ClientMode(dest, port, charset)
        while True:
            if DBG: print("[dbg] ENTER LOOP")
            ret = c.clientCommandHandler()
            if ret == "CONTINUE":
                # continue to send data, create headers, etc.
                hh = HeaderHandler()
                headers = hh.generateOutgoingHeaders("1","2","3","4", message)
                print(headers)
                c.c.send("DATA\r\n".encode(charset))
                c.c.send(headers.encode(charset))
                c.c.send(message.encode(charset))
                c.c.send("\r\n.\r\n".encode(charset))
            elif ret == "SUCCESS":
                c.c.send("QUIT\r\n".encode(charset))
            else:
                break
    else:
        # Chain mode
        if DBG: print("[dbg] Entering CHAIN mode")

        if iplib.hasPort(dest):
            dest = dest.split(":",1)[0]
            port = int(dest.split(":",1)[1])
        else:
            if DBG: print("[dbg] Using default port of {}".format(defport))
            port = defport
        #s = ServerMode(source, port, charset)
        #while True:
            #ret = s.serverCommandHandler()

main()
