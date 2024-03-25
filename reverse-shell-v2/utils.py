import logging
import socket
import sys 
import threading

# to signal to stop the threads 
stop_event = threading.Event()


def close_connection(sock, conn=None):
    """Closes the connection and the socket."""
    if conn:
        conn.close()
        sock.close()
        logging.info("Server is shutdown!")
        sys.exit(0)
    elif sock:
        sock.close()
        logging.info("Server is shutdown!")
        sys.exit(0)


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
                    break  # break from current connection and back to the main terminal.
                print()
                print(data, end="")
                print()

        except socket.error as err:
            logging.error("Error sending or receving data: ", err)
            break
