def check_scanf(string, null_byte=True):
    disallow = ['\n','\r','\x0b', ' ', 0x0C, '\t'] # Bad Bytes
    if null_byte:
        disallow.append(0x00)

    for ch in disallow:
        if str(ch) in string:
            raise Exception("Found: {} in payload".format(repr(ch)))

    return True