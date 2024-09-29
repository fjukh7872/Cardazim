from __future__ import annotations
import socket
import struct
PARTIAL_DATA = "The connenction ended before all of the data was received. "



class Connection():
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self) -> str:
        return f"Connection from {self.connection.getsockname()} to {self.connection.getpeername()}"
    
    def send_message(self, message: bytes):
        self.connection.sendall(struct.pack("<I", len(message)) + message)
    
    def receive_message(self) -> str:
        length = struct.unpack("<I", self.connection.recv(4))[0]
        message = b''
        while len(message) < length:
            data = self.connection.recv(4096)
            if data:
                message += data
            else:
                raise Exception(PARTIAL_DATA)
        message = message.decode()
        return message
    
    @classmethod
    def connect(cls, host: str, port: int) -> Connection:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        return Connection(conn)
    
    def close(self):
        self.connection.close()
    
    def __enter__(self) -> Connection:
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()