#!/usr/bin/python3

import string, pprint, Checksum, iplib, random, platform, sys, datetime

class DataHandler:
    def __init__(self, charset, le):
        self.raw_data = "" # raw data from client
        self.raw_headers = "" # raw headers from client
        self.raw_lheaders = "" # raw headers from client converted to lowercase
        self.raw_message = "" # raw message from client
        self.le = le # line ending the client has been using. We always use /r/n
        self.hdata = {} # header data fields
        self.charset = charset # character set in use
        self.warnings = [] # warnings about the message being parsed
        self.localMessageChecksum = ""

    def parseForHeader(self, search, hopdata):
        search = search.lower()
        for line in hopdata.split(self.le):
            if line.lower().find(search) == 0:
                if search == "hop":
                    return "".join([x for x in line if x in string.digits])
                else:
                    return line.split(":",1)[1].strip()
        return ""

    def headerToDict(self, hop, hopdata):
        for line in self.raw_headers.split(self.le):
            # skip the hop header
            if line.lower().find("hop") != 0 and line.strip() != "":
                try:
                    title, data = [x.strip() for x in line.strip().split(":",1)]
                    if hop not in self.hdata:
                        self.hdata[hop] = {}
                    self.hdata[hop][title.lower()] = data
                except:
                    self.warnings.append("ERROR PARSING HEADER {}".format(hop))

    def parseIncoming(self, data):
        self.raw_data = data

        # seperate headers from message. If this fails, we abort hard. This inciden will be reported.
        try:
            # set the raw_headers and raw_message variables
            self.raw_headers, self.raw_message = self.raw_data.split("{}{}".format(self.le, self.le),1)
        except:
            self.warnings.append("HEADERS NOT SEPERATED FROM MESSAGE. RIP")
            return self.warnings

        # seperate the message from the EOM. If no EOM detected, we just use the rest of the transmission from the client as the message, and throw an error to the client later
        try:
            self.full_message, _ = self.raw_message.split("{}.{}".format(self.le, self.le),1)
            self.full_message = self.full_message.replace("{}..{}".format(self.le, self.le), "{}.{}".format(self.le, self.le))
        except:
            self.full_message = self.raw_message
            self.warnings.append("ERROR, NO EOM DETECTED")

        # create lowercase headers
        self.raw_lheaders = self.raw_headers.lower()

        self.localMessageChecksum = Checksum.checksum(self.full_message, self.charset)

        # split out the hops and begin parsing each one
        hopsplit = ["hop{}".format(x) for x in self.raw_lheaders.split("hop") if x.strip() != ""]
        for hop in hopsplit:
            try:
                # hop number
                hopnum = int(self.parseForHeader("hop", hop))
                # convert rest of headers to a dictionary variable
                self.headerToDict(int(hopnum), hop)
                # take local checksum of hop header
                self.hdata[hopnum]["localheaderschecksum"] = Checksum.checksum(hop, self.charset)
            except Exception as e:
                self.warnings.append("MISSING HOP NUMBER FOR ONE OF THE HOPS")

        # return the produced warnings to the server handler, if desired can be used later.
        return self.warnings

    def getNewHopNum(self):
        return max([x for x in self.hdata]) + 1

    def mkRandNum(self, size):
        return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))

    def createOutgoing(self, destIP, destPort, srcIP, srcPort, message):
        output = ""
        newHeaders = ""
        nhl = []

        hopnum = 0
        mid = str(self.mkRandNum(8))
        if self.raw_headers != "":
            # we have had previous communications
            hopnum = self.getNewHopNum()
            try:
                nmid = self.hdata[hopnum-1]["messageid"]
                if iplib.isInteger(str(nmid)):
                    mid = str(nmid)
            except:
                pass # oh well.

        # generate the new headers
        nhl.append(("Hop",str(hopnum)))
        nhl.append(("MessageId", mid))
        nhl.append(("FromHost", "{}:{}".format(srcIP, srcPort)))
        nhl.append(("ToHost", "{}:{}".format(destIP, destPort)))
        nhl.append(("System", "{} {} {}".format(platform.system(), platform.machine(), platform.release())))
        nhl.append(("Program", "{}/{}".format("Python", platform.python_version())))
        nhl.append(("Author", "Jared Dunbar"))
        tm = datetime.datetime.utcnow()
        nhl.append(("SendingTimestamp", "{:02}:{:02}:{:02}:{:03}".format(tm.hour, tm.minute, tm.second, int(tm.microsecond / 100))))
        nhl.append(("MessageChecksum", Checksum.checksum(message.replace("\r\n.\r\n", "\r\n..\r\n"), self.charset)))

        # build new headers
        newHeaders = "\r\n".join(["{}: {}".format(x ,y) for (x,y) in nhl]) + "\r\n"

        newHeaders += "HeaderChecksum: {}\r\n".format(Checksum.checksum(newHeaders, self.charset))

        # new headers slapped on top
        output += newHeaders
        # Old headers slapped on bottom
        output += self.raw_headers
        # Header and Body seperator
        output += "\r\n"
        # Message (properly encoded)
        output += message.replace("\r\n.\r\n", "\r\n..\r\n")
        # EOM
        output += "\r\n.\r\n"
        return output
