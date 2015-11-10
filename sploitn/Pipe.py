class Pipe(object):

    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    def __init__(self, debug, debug_bufflim=60,color=True):
        self.debug = debug
        self.color = color
        self.debug_bufflim = debug_bufflim
        if debug and debug_bufflim is not None:
            self.red('Warning: Buffer output limited to {} '\
                'chars'.format(debug_bufflim), char=' ! ')

    def colored(self, text, color):
        if self.color:
            return color + str(text) + self.ENDC

        return text

    def info(self, text, char=' + ', color=PURPLE):
        print("{}[{}]{} {}".format(
            color,
            char,
            self.ENDC,
            text
        ))
    def red(self, text, char=' - '):
        self.info(
            self.colored(text, color=self.RED),
            char=char
        )

    def read_byte(self):
        raise NotImplementedError()

    def send(self, s):
        raise NotImplementedError()

    def interact(self):
        self.red('Beginning interaction...')
        self._interact()

    def _interact(self):
        raise NotImplementedError()

    def _send(self,s):
        raise NotImplementedError()

    def info_with_snip(self, s, *args, **kwargs):
        if self.debug_bufflim and len(s) > self.debug_bufflim:
            self.info(repr(s[:self.debug_bufflim] + '... ({} more chars)'.format(
                len(s) - self.debug_bufflim
            )),color=self.GREEN, *args, **kwargs)
        else:
            self.info(repr(s), color=self.GREEN, *args, **kwargs)

    def read_n(self, n):
        s = ''
        for _ in xrange(n):
            try:
                s += self.read_byte()
            except (EOFError, KeyboardInterrupt):
                if self.debug:
                    self.info_with_snip(s,char='<..')
                raise
        if self.debug:
            self.info_with_snip(s,char='<<<')
        return s

    def read_until(self, sentinel='\n'):
        s = ''
        while not s.endswith(sentinel):
            #b = read_byte()
            #sys.stdout.write(b)
            #sys.stdout.flush()
            try:
                s += self.read_byte()
            except (EOFError, KeyboardInterrupt):
                if self.debug:
                    self.info_with_snip(s,char='<..')
                raise
        if self.debug:
            self.info_with_snip(s,char='<<<')
        return s

    def send(self, s):
        if self.debug:
            self.info_with_snip(s, char='>>>')
        self._send(s)
