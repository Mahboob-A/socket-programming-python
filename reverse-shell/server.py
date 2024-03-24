import socket 
import sys 
import logging

from config import HOST, PORT


def create_socket(): 
        ''' Creates a socket object. '''
        try:     
                # TCP connection 
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                logging.info('socket creation successful!')
                return sock             
        except socket.error as err: 
                logging.error('Socket creation error:  ', err)
                sys.exit(1)


def bind_socket(sock): 
    """Binds the socket to the specified host and port."""
    try:
        # binding and listening to at most 2 connections
        sock.bind((HOST, PORT))
        sock.listen(2)
        logging.info(
                f"server is listening in host:  {'open-to-all' if HOST == '' else HOST} and port:  {PORT}"
        )
    except socket.error as err:
        logging.error("Socket binding error:  ", err)
        logging.info('Retrying to bind socket...')
        # call the helper function to retry to bind the socket. 
        retry_bind_socket_helper(sock)


def retry_bind_socket(sock):
    """Retries to bind the socket to the specified host and port."""
    try:
        # binding and listening to at most 2 connections
        sock.bind((HOST, PORT))
        sock.listen(2)
        logging.info(
            f"server is listening in host:  {'open-to-all' if HOST == '' else HOST} and port:  {PORT}"
        )
        return True 
    except socket.error as err:
        logging.error("Socket binding error:  ", err)
        logging.info("Retrying to bind socket...")
        return False 


def retry_bind_socket_helper(sock):
    '''Helper function to retury to bind to the speific HOST and PORT for 5 times. ''' 
    retry = 5
    
    while retry >= 0: 
        result = retry_bind_socket(sock)
        if not result:
                retry -= 1
        else: 
                break

    if retry == 0:
        logging.error("Failed to bind to connection!")
        logging.info("Retried to bind the socket upto 5 times")


def accept_socket(sock): 
        ''' Accepts a connection from a client. '''
        try: 
                conn, addr = sock.accept()
                logging.info(f"Connected to address:  {addr[0]} and port:  {addr[1]}")
                return conn, addr
        except socket.error as err:
                logging.error("Error accepting the connection: ", err)


def commands_handler(conn, s): 
    """Sends commands to the clinet. """
    logging.info("Sending commands to client... ")
    while True:
        command = input("Enter command ('q' to exit)...   ")
        if command.strip() == "":
            print("Command can not be empty. please try again.")
            continue
        if command == "q":
            break

        encoded_command = command.encode("utf-8")
        if len(encoded_command) > 0:
            conn.send(encoded_command)
            data = conn.recv(1024).decode("utf-8")  # str(conn.recv(1024), 'utf-8')
            print(data, end="")


def close_connection(sock, conn=None):
    """Closes the connection and the socket."""
    if conn: 
        conn.close()
        sock.close()
        logging.info("Server is shutdown!")
        sys.exit(0)
    else: 
        sock.close()
        logging.info("Server is shutdown!")
        sys.exit(0)

def main(): 
        logging.basicConfig(level=logging.INFO)
        logging.info('Starting server...')
        
        # Create and bind the socket 
        sock = create_socket()
        bind_socket(sock)
        conn = None 
        try: 
                conn, addr = accept_socket(sock=sock)
                commands_handler(conn)
                # close the connection and the socket as the user pressed 'q' 
                close_connection(sock, conn)
        except KeyboardInterrupt: 
                logging.info('Server shutdown initiated by user.')
                # close the connection and the socket as the user pressed 'ctrl-c'
                # if server is stopped as ctrl-c before any connection has established, 
                # then conn will be unavailable. 
                if conn is not None: 
                        close_connection(conn, sock)
                else: 
                        close_connection(sock)


if __name__ == '__main__': 
        main()

