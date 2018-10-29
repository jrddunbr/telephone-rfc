#!/usr/bin/python3

import string, pprint, Checksum

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
                    self.hdata[hop][title] = data
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
        except:
            self.full_message = self.raw_message
            self.warnings.append("ERROR, NO EOM DETECTED")

        # create lowercase headers
        self.raw_lheaders = self.raw_headers.lower()

        self.localMessageChecksum = Checksum.checksum(self.full_message, self.charset)
        print("Local Message Checksum: {}".format(self.localMessageChecksum))

        # split out the hops and begin parsing each one
        hopsplit = ["hop{}".format(x) for x in self.raw_lheaders.split("hop") if x.strip() != ""]
        for hop in hopsplit:
            try:
                hopnum = int(self.parseForHeader("hop", hop))
                self.headerToDict(int(hopnum), hop)
                chksum = Checksum.checksum(hop, self.charset)
                self.hdata[hopnum]["LocalHeadersChecksum"] = chksum
            except Exception as e:
                print(e)
                self.warnings.append("MISSING HOP NUMBER FOR ONE OF THE HOPS")


        pprint.pprint(self.hdata)
        print()
        print("`{}`".format(self.full_message))

        # return the produced warnings to the server handler, if desired can be used later.
        return self.warnings
