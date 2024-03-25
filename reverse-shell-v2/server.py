import socket
import sys
import logging
from time import sleep
import threading

from config import(
    HOST, PORT, MAX_BIND_RETRIES, NUMBER_OF_THREADS, JOB_NUMBER, 
    ALL_CONNECTIONS, ALL_ADDRESSES, Q 
)
from shell import terminal
from utils import close_connection

from queue import Queue

server_socket_dict = {}


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


def bind_socket_helper(sock):
    """Binds to bind the socket to the specified host and port."""
    try:
        # binding and listening to any number of connections 
        sock.bind((HOST, PORT))
        sock.listen()
        return True
    except socket.error as err:
        logging.error("Socket binding error:  %s", err)
        logging.info("Retrying to bind socket...")
        return False


def bind_socket(sock):
    """Entry function to bind to the speific HOST and PORT."""
    for attempt in range(MAX_BIND_RETRIES + 1):  # MAX_BIND_RETRIES = 5
        bind_successful = bind_socket_helper(sock)
        if bind_successful:
            return True
            # continue # continue to reproduce the error
        else:
            logging.error("Socket binding error attempt %d:  ", attempt)
            if attempt == MAX_BIND_RETRIES:
                logging.error(
                    "Failed to bind to the connection after {} retries.".format(
                        MAX_BIND_RETRIES
                    )
                )
                return False
        # wait before retrying to bind again 
        sleep(0.8)


def accept_socket_helper(sock): 
    ''' Helper function to accept multiple socket connctions. '''
    if sock is not None: 
        try: 
            while True: 
                conn, addr = sock.accept()
                logging.info(f"Connected to address:  {addr[0]} and port:  {addr[1]}")
                ALL_CONNECTIONS.append(conn)
                ALL_ADDRESSES.append(addr)
        except socket.error as err:
            logging.error("Error accepting the connection: ", err)
            raise 
    else: 
        logging.error(
            'Server socket is None! The possible error might be the bind is unsuccessful. Check if \
            the binding has been successful. '
        )


def accept_socket(sock):
    """Accepts a connection from a client."""
    try:
        accept_socket_helper(sock)
    except socket.error as err:
        logging.error(
            "Could not accept the incoming connection from accept_socket_helper(): ", err
        )


def create_server_socket(): 
    ''' Create the socket object for the server. '''
    # Create and bind the socket
    sock, err = create_socket()
    if sock:
        bind_successful = bind_socket(sock)
        if bind_successful:
            logging.info("Server bind successful!")
            logging.info(
                f"Server is listening to host:  {'open-to-all' if HOST == '' else HOST} and port:  {PORT}"
            )
            # put the sock object in the dict. 
            server_socket_dict['sock'] = sock
        else:
            logging.error(
                "Aborting the Server Bind: Bind could not be established after multiple retries!"
            )
    else:
        logging.error("Aborting the Server Socket Creation: Server socket could not be created: %s", err)


# Entrypont for thread 1 - handling connections.
def handle_connections(): 
    '''Entry function for handling multiple connections. '''

    sock = server_socket_dict.get('sock', None)
    if sock is None: 
        create_server_socket()
    conn = None 
    try:
        sock = server_socket_dict.get('sock')
        # thread 01. accept multiple connections.
        conn, addr = accept_socket(sock=sock)
    except (Exception, KeyboardInterrupt):
        logging.info("Server shutdown initiated by user.")
        if conn is not None:
            close_connection(conn, sock)
        else:
            close_connection(sock)    


# Entrypont for 2nd thread - terminal
def handle_command_communications(): 
    # thread 02. handle interaction with multiple connections.
    sock = server_socket_dict.get('sock', None)
    # if sock is not None:
    #     print('sock: ', sock)
    print("sock outside if: ", sock)
    terminal(sock=sock)
