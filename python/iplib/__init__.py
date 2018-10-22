class iplib:
    # If good address, return True
    def checkIPv4(addr):
        good = True
        octets = addr.split(".")
        if(len(octets)) == 4:
            for octet in octets:
                if not (octet >= 0 and octet <= 255):
                    good = False
        else:
            good = False
        return good

    # If good address, return True
    def checkIPv4maybePort(addr):
        if ":" in addr:
            ip, port = addr.split(":",1)
            good = checkIPv4(ip)
            try:
                _ = int(port)
                return good
            except:
                return False
        else:
            return checkIPv4(addr)
