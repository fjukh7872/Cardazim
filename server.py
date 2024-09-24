import argparse
import sys
import struct
import socket
import threading



def single_client(conn: socket, addr : tuple[str, int]):
    '''
    Handling a single client.
    '''
    length = struct.unpack("<I", conn.recv(4))[0]
    message = b''
    while len(message) < length:
        message += conn.recv(4096)
    message = message.decode()
    print(f"Received data: {message}")
    conn.close()


def run_server(ip: str, port: int):
    '''
    Running the entire server with the provided ip and port.
    '''
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((ip, port))
    while True:
        serv.listen()
        conn, addr = serv.accept()
        print(addr)
        threading.Thread(target = single_client, args = (conn, addr)).start()


def get_args():
    parser = argparse.ArgumentParser(description='Receive data from client.')
    parser.add_argument('ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.ip, args.port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
