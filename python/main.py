#!/usr/bin/python3

import socket, time, datetime, os, sys, iplib, string, random, platform
from DataHandler import DataHandler

DBG = True
HLP = False
CHARSET = "ascii"

def mkRandNum(size):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))

def clientMode(newIP, newPort, input):
    output = ""
    c = socket.socket()
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c.connect((newIP, newPort))
    haylo = c.recv(64).decode(CHARSET)
    if haylo.find("HELLO 1.7.1") != 0:
        # invalid HELLO sequence, time to say goodbye!
        c.send("QUIT\r\n".encode(CHARSET))
        c.close()
    c.send("HELLO 1.7.1\r\n".encode(CHARSET))
    print("HELLO!")
    LE = "\r\n"
    if "\r" not in haylo:
        # bad line ending
        print("Client uses bad line endings!")
        LE = "\n"
    dh = None
    if isinstance(input, DataHandler):
        dh = input
    else:
        dh = DataHandler(CHARSET, LE)
        dh.full_message = input
    dh.srcIP = newIP
    dh.srcPort = newPort
    output = dh.createOutgoing(newIP, newPort, dh.full_message)
    okay = c.recv(256).decode(CHARSET)
    print(okay)
    if okay.find("OK") != 0:
        print("NOT OK")
        c.send("QUIT\r\n".encode(CHARSET))
        c.close()
    c.send("DATA\r\n".encode(CHARSET))
    okay = c.recv(256).decode(CHARSET)
    if okay.find("OK") != 0:
        print("DEF NOT OK")
        c.send("QUIT\r\n".encode(CHARSET))
        c.close()
    c.send(output.encode(CHARSET))
    wrnsucc = c.recv(32).decode(CHARSET)
    c.send("QUIT\r\n".encode(CHARSET))
    c.close()

def serverMode(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port - 1))
    print("Listening on port {}".format(port - 1))
    s.listen()
    while True:
        c, (clientIP, clientPort) = s.accept()
        print("Connection estabilished from {}:{}".format(clientIP, clientPort))
        c.send("HELLO 1.7.1\r\n".encode(CHARSET))
        ret =  c.recv(32).decode(CHARSET)
        if ret.find("HELLO 1.7.1") != 0:
            # invalid HELLO sequence, time to say goodbye!
            c.send("GOODBYE\r\n".encode(CHARSET))
            c.close()
        LE = "\r\n"
        if "\r" not in ret:
            # bad line ending
            print("Client uses bad line endings!")
            LE = "\n"
        dh = DataHandler(CHARSET, LE)
        dh.srcIP = clientIP
        dh.srcPort = clientPort
        okmsg = ""
        if LE == "\n":
            okmsg = " BTW, you're not using CRLF. netcat help: DATA<headers><crlf><data><eom>QUIT"
        c.send("OK welcome!{}\r\n".format(okmsg).encode(CHARSET))
        done = False
        while not done:
            action = c.recv(16).decode(CHARSET)
            if "DATA" in action:
                c.send("OK go ahead...\r\n".encode(CHARSET))
                raw_data = ""
                while "{}.{}".format(LE, LE) not in raw_data:
                    raw_data += c.recv(1024).decode(CHARSET)
                warnings = dh.parseIncoming(raw_data)
                done = True
                try:
                    if len(warnings) > 0:
                        c.send("WARN\r\n".encode(CHARSET))
                    else:
                        c.send("SUCCESS\r\n".encode(CHARSET))
                    c.recv(16) # meh, QUIT whether you like it or not.
                    c.send("GOODBYE\r\n".encode(CHARSET))
                    c.close()
                except Exception as e:
                    print("Client closed early. {}".format(e))
            elif "QUIT" in action:
                c.send("GOODBYE\r\n".encode(CHARSET))
                c.close()
            else:
                c.send("NOK not a recognized command.\r\n".encode(CHARSET))
        c.close()
        return dh

def printUsage():
    print("""Usage:\n
python3 main.py [mode] (destIP:destPort)
where:
* mode is the mode of the program, either init or chain mode (default chain mode)
* destIP:destPort where destIP is the next hop, and destPort is the port to use
""")
    sys.exit(0)

def main():
    global HLP

    mode = False # False is chain, True is origin
    combDest = ""
    if len(sys.argv) == 2:
        combDest = sys.argv[1]
    elif len(sys.argv) == 3:
        mode = ("init" in sys.argv[1])
        combDest = sys.argv[2]
    else:
        printUsage()

    dest = ""
    destPort = 32409
    if iplib.hasPort(combDest):
        dest = combDest.rsplit(":",1)[0]
        destPort = int(combDest.rsplit(":",1)[1])
    else:
        dest = combDest

    destIP = socket.gethostbyname(dest)

    if not iplib.checkIPv4maybePort("{}:{}".format(destIP, destPort)):
        print("Error, {}:{} is not a valid IP address and port.".format(destIP, destPort))

    if mode:
        # origination mode
        f = open("message.txt")
        message = "\n".join(f.read())
        f.close()

        clientMode(destIP, destPort, message)
    else:
        # chain mode
        while 1:
            clientMode(destIP, destPort, serverMode(destPort))
            return

main()
