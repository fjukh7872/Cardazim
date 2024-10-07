import argparse
import sys
import threading
import listener



def single_client(conn: listener.connection.Connection):
    '''
    Handling a single client.
    '''
    print(f"Received data: {conn.receive_message()}")
    conn.close()


def run_server(ip: str, port: int):
    '''
    Running the entire server with the provided ip and port.
    '''
    with listener.Listener(port, ip) as lstnr:
        while True:
            conn = lstnr.accept()
            threading.Thread(target = single_client, args = (conn,)).start()


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
