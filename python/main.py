#!/usr/bin/python3

import socket, time, datetime, os, sys, iplib, string, random, platform
from DataHandler import DataHandler

DBG = True
HLP = False

def mkRandNum(size):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))

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
    undest = "" # possibly errored and with port potentially
    dest = "" # definte destination IP only.
    source = "0.0.0.0" # default source address - any address
    defport = 32409
    mode = False # False is not originiate, ie, chain mode
    charset = "ascii"
    if len(sys.argv) == 2:
        # undest
        undest = sys.argv[1]
    elif len(sys.argv) == 3:
        # undest, mode
        undest = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms == "init") or (ms == "start")
    elif len(sys.argv) == 4:
    # dest, mode, source
        undest = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms ==  "init") or (ms == "start")
        charset = sys.argv[3]
    elif len(sys.argv) == 5:
    # dest, mode, source
        undest = sys.argv[1]
        ms = sys.argv[2].lower().strip()
        mode = (ms == "0") or (ms == "o") or (ms == "originator") or (ms == "init") or (ms == "start")
        charset = sys.argv[3]
        source = sys.argv[4]
    else:
        # error, do the usage dialog
        printUsage()

    if not iplib.checkIPv4maybePort(undest):
        print("[err] Sorry, but {} is not a valid IPv4 address".format(undest))
        sys.exit(1)

    if not iplib.checkIPv4maybePort(source):
        print("[err] Sorry, but {} is not a valid IPv4 address".format(source))
        sys.exit(1)

    if charset not in ["utf-8", "ascii"]:
        print("[err] Invalid Charset")
        sys.exit(1)

    if DBG: print("[dbg] stuff looks good. starting")
    if DBG: print("dest: {}\nsource: {}\ncharset: {}\nmode: {}".format(undest, source, charset, mode))

    if mode:
        # origination mode
    else:
        # chain mode

main()
