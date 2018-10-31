#!/usr/bin/python3

import socket, time, datetime, os, sys, iplib, string, random, platform
from DataHandler import DataHandler

DBG = True
HLP = False
charset = "ascii"

def mkRandNum(size):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))


def clientMode():
    pass


def serverMode():
    pass


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

    if not checkIPv4maybePort("{}:{}".format(destIP, destPort)):
        print("Error, {}:{} is not a valid IP address and port.".format(destIP, destPort))

    if mode:
        # origination mode
        clientMode(destIP, destPort)
    else:
        # chain mode
        while 1:
            clientMode(serverMode(destPort))

main()
