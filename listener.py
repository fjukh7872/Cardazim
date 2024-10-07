
from __future__ import annotations
import socket
import connection
DEFAULT_BACKLOG = 1000



class Listener:
    def __init__(self, port: int, host: str, backlog = DEFAULT_BACKLOG):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind((host, port))
        self.backlog = backlog

    def __repr__(self) -> str:
        return f"Listener(port={self.serv.getsockname()[1]}, host={self.serv.getsockname()[0]}, backlog={self.backlog})"
    
    def start(self):
        self.serv.listen(self.backlog)
    
    def stop(self):
        self.serv.close()
    
    def accept(self) -> connection.Connection:
        return connection.Connection(self.serv.accept()[0])

    def __enter__(self) -> Listener:
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop()