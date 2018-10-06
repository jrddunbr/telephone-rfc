class iplib:
    # If good address, return true
    def checkIPv4(addr):
        bad = True
        octets = addr.split(".")
        if(len(octets)) == 4:
            bad = False
            for octet in octets:
                if not (octet >= 0 and octet <= 255):
                    bad = True
        return not bad
