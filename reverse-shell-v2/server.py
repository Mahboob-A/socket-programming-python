import socket
import sys
import logging

from config import(
    HOST, PORT, MAX_BIND_RETRIES, NUMBER_OF_THREADS, JOB_NUMBER, 
    ALL_CONNECTIONS, ALL_ADDRESSES, Q 
)


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
        # binding and listening to at most 2 connections
        sock.bind((HOST, PORT))
        sock.listen(2)
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


def accept_socket(sock):
    """Accepts a connection from a client."""
    try:
        conn, addr = sock.accept()
        logging.info(f"Connected to address:  {addr[0]} and port:  {addr[1]}")
        return conn, addr
    except socket.error as err:
        logging.error("Error accepting the connection: ", err)


def commands_handler(conn, sock):
    """Sends commands to the clinet."""
    logging.info("Sending commands to client... ")
    while True:
        command = input("Enter command ('q' to exit)...   ")
        if command.strip() == "":
            print("Command can not be empty. please try again.")
            continue
        if command == "q":
            break

        try:
            encoded_command = command.encode("utf-8")
            if len(encoded_command) > 0:
                conn.send(encoded_command)
                data = conn.recv(1024).decode("utf-8")  # str(conn.recv(1024), 'utf-8')
                if not data:
                    close_connection(conn=conn, sock=sock)
                print()
                print(data, end="")
                print()
        except socket.error as err:
            logging.error("Error sending or receving data: ", err)
            break


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
    logging.info("Starting server...")

    # Create and bind the socket
    sock, err = create_socket()
    if sock:
        bind_successful = bind_socket(sock)
        if bind_successful:
            logging.info("Connection bind successful!")
            logging.info(
                f"server is listening to host:  {'open-to-all' if HOST == '' else HOST} and port:  {PORT}"
            )
            conn = None
            try:
                conn, addr = accept_socket(sock=sock)
                commands_handler(conn, sock)
                # close the connection and the socket as the user pressed 'q'
                close_connection(conn=conn, sock=sock)
            except KeyboardInterrupt:
                logging.info("Server shutdown initiated by user.")
                # close the connection and the socket as the user pressed 'ctrl-c'
                # if server is stopped as ctrl-c before any connection has established,
                # then conn will be unavailable.
                if conn is not None:
                    close_connection(conn, sock)
                else:
                    close_connection(sock)
        else:
            logging.error(
                "Aborting the connection: connection could not be established multiple retries!"
            )
    else:
        logging.error("Aborting the connection: socket could not be created: %s", err)


if __name__ == "__main__":
    main()
