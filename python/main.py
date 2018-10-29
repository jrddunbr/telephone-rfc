#!/usr/bin/python3

import socket, time, datetime, os, sys, iplib, string, random, platform

DBG = True
HLP = False

def mkRandNum(size):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))

class HeaderHandler:
    def __init__(self, charset):
        self.raw_headers = ""
        self.hop = {}
        self.lhd = "" # Latest HeaDers sent
        self.charset = charset

    def feedIncomingHeaders(self, headerString):
        self.raw_headers = headerString
        self.lraw_headers = self.raw_headers.lower()

    def getThisHopNum(self):
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
        mid = str(mkRandNum(8))
        myHop = 0
        if self.raw_headers == "":
            # generate initial header variables
            pass
        else:
            mid = self.getMessageId()
            myHop = self.getThisHopNum()
        # generate new headers on top of the existing headers
        self.hop[myHop] = {}
        self.hop[myHop]["Hop"] = str(0)
        self.hop[myHop]["MessageId"] = mid
        self.hop[myHop]["FromHost"] = "{}:{}".format(src, srcp)
        self.hop[myHop]["ToHost"] = "{}:{}".format(dest, destp)
        self.hop[myHop]["System"] = "{} {} {}".format(platform.system(), platform.machine(), platform.release())
        self.hop[myHop]["Program"] = "{}/{}".format("Python", platform.python_version())
        self.hop[myHop]["Author"] = "Jared Dunbar"
        tm = datetime.datetime.utcnow()
        self.hop[myHop]["SendingTimestamp"] = "{}:{}:{}:{}".format(tm.hour, tm.minute, tm.second, int(tm.microsecond / 100))
        self.hop[myHop]["MessageChecksum"] = checksum(msg.encode(self.charset))
        self.ldh = ""
        for hd in self.hop[myHop]:
            self.lhd += str("{}: {}\r\n".format(hd, self.hop[myHop][hd]))
        if self.raw_headers != "":
            self.lhd = raw_headers + self.lhd
        return self.lhd

    def getHeaderSum(self):
        hcsm = checksum(self.lhd.encode(self.charset))
        return "HeaderChecksum: {}\r\n".format(hcsm)

class ClientMode:
    def __init__(self, serverIP, serverPort, charset):

        # Initialization of variables
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.charset = charset
        self.tr = "\r\n"
        self.version = "1.7.1"
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
            self.c.send("GOODBYE\r\n".encode(self.charset))
            self.c.close()
        if data == "SUCCESS{}".format(self.tr):
            return "SUCCESS"
        if data == "GOODBYE".format(self.tr):
            self.c.close()
            return "TERMINATE"
        if data == "WARN{}".format(self.tr):
            return "WARN"

class ServerMode:
    def __init__(self, listenIP, listenPort, charset):

        # Initialization of variables
        self.listenIP = listenIP
        self.listenPort = listenPort
        self.charset = charset
        self.tr = "\r\n"
        self.version = "1.7.1"
        self.warningHeaders = []

        # Construct the server socket
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if DBG: print("[dbg] binding server to {}:{}".format(self.listenIP, self.listenPort))
        self.s.bind((self.listenIP, self.listenPort))
        self.s.listen()
        if DBG: print("[dbg] listening?")

    def parseData(self, socket):
        data = c.recv(2048).decode(self.charset)
        lines = data.split(lr)
        end = -1
        for x in range(0, len(lines)):
            if lines[x] == ".":
                end = x
        if end == -1:
            print("[err] Non compliance detected, there is no end of message, indicated by  <CRLF>.<CRLF>")
            self.warningHeaders.append("No EOM detected")

    def serverCommandHandler(self, c):
        data = c.recv(256).decode(self.charset)
        if DBG: print("[dbg] SCH init")
        if DBG: print(data)
        if "\r" not in data:
            self.tr = "\n"
            print("[err] Newlines are not CRLF")
            self.warningHeaders.append("Newlines are not in CRLF form")
        if data == "HELLO {}{}".format(self.version, self.tr):
            if DBG: print("[dbg] Hello complete.")
            return "CONTINUE"
        elif "HELLO" in data:
            print("[err] Client Telephone Version Incompatible")
            c.send("GOODBYE\r\n".encode(self.charset))
            c.close()
        if data == "DATA{}".format(self.tr):
            return "DATA"
        if data == "QUIT".format(self.tr):
            c.send("GOODBYE\r\n".encode(self.charset))
            c.close()
            return "TERMINATE"

    def serverInstance(self):
        inHeaders = ""
        inData = ""
        warningHeaders = []
        c, caddr = self.s.accept()
        c.send("HELLO {}\r\n".format(self.version).encode(self.charset))
        # Recieve HELLO version from Client
        run = True
        while run:
            action = self.serverCommandHandler(c)
            if action == "CONTINUE":
                pass
            if action == "DATA":
                self.parseData(c)
            if action == "TERMINATE":
                run = False
        return inHeaders, inData

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
    global HLP
    deste = "" # possibly errored and with port potentially
    dest = "" # definte destination IP only.
    source = "0.0.0.0" # default source address - any address
    defport = 32409
    mode = False # False is not originiate, ie, chain mode
    charset = "ascii"
    if len(sys.argv) == 2:
        # deste
        deste = sys.argv[1]
    elif len(sys.argv) == 3:
        # deste, mode
        deste = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms == "init") or (ms == "start")
    elif len(sys.argv) == 4:
    # dest, mode, source
        deste = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms ==                 hh = HeaderHandler(charset)
 "init") or (ms == "start")
        charset = sys.argv[3]
    elif len(sys.argv) == 5:
    # dest, mode, source
        deste = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms == "init") or (ms == "start")
        charset = sys.argv[3]
        source = sys.argv[4]
    else:
        # error, do the usage dialog
        printUsage()

    if not iplib.checkIPv4maybePort(deste):
        print("[err] Sorry, but {} is not a valid IPv4 address".format(deste))
        sys.exit(1)

    if not iplib.checkIPv4maybePort(source):
        print("[err] Sorry, but {} is not a valid IPv4 address".format(source))
        sys.exit(1)

    if charset not in ["utf-8", "ascii"]:
        print("[err] Invalid Charset")
        sys.exit(1)

    if DBG: print("[dbg] stuff looks good. starting")
    if DBG: print("dest: {}\nsource: {}\ncharset: {}\nmode: {}".format(deste, source, charset, mode))
                 hh = HeaderHandler(charset)

    if mode:
        # Origination mode
        if DBG: print("[dbg] Entering ORIGIN mode")
        message = input("Input message:\n")
        print("=======\nMessage:")
        print(message)
        if iplib.hasPort(deste):
            if DBG: print(deste.split(":",1))
            dest = deste.split(":",1)[0]
            port = int(deste.split(":",1)[1])
        else:
            if DBG: print("[dbg] Using default port of {}".format(defport))
            port = defport
        c = ClientMode(dest, port, charset)
        src = c.c.getsockname()[0]
        srcp = c.c.getsockname()[1]
        while True:
            if DBG: print("[dbg] ENTER LOOP")
            if HLP: print("[hlp] On server, type either \"HELLO 1.7\", \"SUCCESS\", \"WARN\" or \"GOODBYE\"")
            ret = c.clientCommandHandler()
            if c.tr == "\n": HLP = True
            # if this server looks like they are not using \r\n, they may be using telnet or netcat to communicate. Send help messages to the client stdout to show how to act as a server just in case you forget :)
            if ret == "CONTINUE":
                # continue to send data, create headers, etc.
                hh = HeaderHandler(charset)
                # dest, destp, src, srcp, msg
                headers = hh.generateOutgoingHeaders(dest, port, src, srcp, message)
                #print(headers)
                c.c.send("DATA\r\n".encode(charset))
                c.c.send(headers.encode(charset))
                c.c.send(hh.getHeaderSum().encode(charset))
                c.c.send("\r\n".encode(charset))
                c.c.send(message.encode(charset))
                c.c.send("\r\n.\r\n".encode(charset))
            elif ret == "SUCCESS":
                c.c.send("QUIT\r\n".encode(charset))
            elif ret == "WARN":
                print("Server responds WARN!")
                c.c.send("QUIT\r\n".encode(charset))
            else:
                break
    else:
        # Chain mode
        if DBG: print("[dbg] Entering CHAIN mode")

        if iplib.hasPort(deste):
            dest = deste.split(":",1)[0]
            port = int(deste.split(":",1)[1])
        else:
            if DBG: print("[dbg] Using default port of {}".format(defport))
            port = defport
        s = ServerMode(dest, port, charset)
        while True:
            inHeaders, inData = s.serverInstance()
main()
