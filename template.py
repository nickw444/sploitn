import struct
from sploitn import encode, LocalPipe, RemotePipe
from sploitn.sane import check_scanf

def main(argv):
    debug = '-d' in argv
    if '-l' in argv:
        # Run Locally
        expl = LocalPipe('./program', debug=debug, wait='-w' in argv)
    else:
        # Run Remote
        PORT = 0000
        HOST = ''
        expl = RemotePipe(HOST, PORT, debug=debug)


if __name__ == '__main__':
    import sys
    main(sys.argv)
