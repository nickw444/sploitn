from subprocess import PIPE, Popen
from .Pipe import Pipe
import os, stat
import time
import threading

class LocalFifoPipe(Pipe):

    def fifo_exists(self, fifo):
        try:
            return stat.S_ISFIFO(os.stat(fifo).st_mode)
        except Exception, e:
            return False

    def __init__(self, executable, args=None, wait=False, stdin='/tmp/fifo.in', stdout='/tmp/fifo.out', *kargs, **kwargs):
        super(LocalFifoPipe, self).__init__(*kargs, **kwargs)

        if args is None:
            args = []

        self.info('Generating fifos')

        fifos = [stdin, stdout]
        for fifo in fifos:
            if not self.fifo_exists(fifo):
                result = os.system('mkfifo {}'.format(fifo))
                if result == 0:
                    self.info('Created fifo: {}'.format(fifo))
                else:
                    self.red('Unable to create fifo: {}'.format(fifo))
                    exit(1)


        self.executable = executable
        args = list(map(lambda x: '"{}"'.format(x), args)) # Quote all args
        args.insert(0, executable)

        self.info("Please run: cat {stdin} - | {executable} > {stdout}".format(
            executable=' '.join(args),
            stdout=stdout,
            stdin=stdin,
        ))

        
        self.stdout = open(stdout)
        self.stdin = open(stdin, 'w')

        self.red("Execution has begun...")
        if os.system('ps ax | grep -v "grep" | grep "{}" > /dev/null'.format(executable)) == 0:
            
            p = Popen('ps ax | grep -v "grep" | grep "{}" | cut -d" " -f 2'.format(executable), stdout=PIPE, shell=True)
            out, err = p.communicate(input='')
            self.info("Program is running with pid: {}".format(
                self.colored(out.strip(), self.RED)
            ))

        if wait:
            wait = raw_input('[ + ] Waiting... Press return to continue...')


    def read_byte(self):
        buf = self.stdout.read(1)
        if not buf:
            raise EOFError
        return buf

    def _send(self, s):
        self.stdin.write(s)

    def _interact(self):
        self.stdin.close() # STDIN needs to come from term now
        self.red('stdin was closed. Use process terminal to enter stdin')
        while True:
            self.info('' + repr(self.read_until())),



