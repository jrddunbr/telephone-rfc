# return True if an integer, if not an integer, return False
def isInteger(yant):
    try:
        _ = int(yant)
        return True
    except:
        return False

# return an integer, if not an integer, return -1
def getInteger(yant):
    try:
        x = int(yant)
        return x
    except:
        return -1

# If good address, return True
def checkIPv4(addr):
    good = True
    octets = addr.split(".")
    if(len(octets)) == 4:
        for octet in octets:
            if not (getInteger(octet) >= 0 and getInteger(octet) <= 255):
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

def hasPort(addr):
    return ":" in addr
