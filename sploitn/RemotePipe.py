import socket
from .Pipe import Pipe

class RemotePipe(Pipe):

    def __init__(self, host, port, *args, **kwargs):
        super(RemotePipe, self).__init__(*args, **kwargs)
        self.host = host
        self.port = port
        self.sock = socket.create_connection((host, port))

    def read_byte(self):
        buf = self.sock.recv(1)
        if not buf:
            raise EOFError
        return buf

    def _send(self, s):
        self.sock.sendall(s)

    def _interact(self):
        import telnetlib

        t = telnetlib.Telnet()
        t.sock = self.sock
        try:
            t.interact()
        except KeyboardInterrupt as e:
            return 
        
