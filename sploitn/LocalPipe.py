from subprocess import PIPE, Popen
from .Pipe import Pipe
import time
import sys

class LocalPipe(Pipe):

    def __init__(self, executable, exec_name=None, args=None, wait=False, *kargs, **kwargs):
        super(LocalPipe, self).__init__(*kargs, **kwargs)

        if args is None:
            args = []
        
        if exec_name:
            args.insert(0, exec_name)
        else:
            args.insert(0, executable)    

        self.executable = executable
        self.subprocess = Popen(args, executable=executable,shell=False, stdout=PIPE, stdin=PIPE, bufsize=0)

        self.info("Subprocess Started with PID: {}".format(
            self.colored(self.subprocess.pid, self.RED)
        ))

        if wait:
            wait = raw_input('[ + ] Waiting... Press return to continue...')


    def read_byte(self):
        buf = self.subprocess.stdout.read(1)
        if not buf:
            raise EOFError
        return buf

    def _send(self, s):
        self.subprocess.stdin.write(s)

    def _interact(self):
        import select, sys, os
        # Monkey Patch ARGV for No Buffer!
        sys.stdin = os.fdopen(sys.stdin.fileno(), 'r', 0)

        buff = ""
        input_buffer = ""
        c = 0

        while True:
            r, w, e = select.select([self.subprocess.stdout, sys.stdin], [self.subprocess.stdin, sys.stdout], [], 0.01)
            # print(r, w, e)
            if self.subprocess.stdout in r:
                input_buffer += self.subprocess.stdout.read(1)

            if sys.stdin in r:
                buff += sys.stdin.read(1)

            if self.subprocess.stdin in w and len(buff) and buff.endswith('\n'):
                self.send(buff)
                buff = ""

            if input_buffer.endswith('\n'):
                if self.debug:
                    self.info_with_snip(input_buffer, char='<<<')
                
                print(input_buffer),

                input_buffer = ""
                c = 0

