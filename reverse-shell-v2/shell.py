import logging
from time import sleep

from config import ALL_CONNECTIONS, ALL_ADDRESSES
from utils import commands_handler, close_connection, stop_event

import threading



'''
Interactive terminal shell for handling all the connections simultaniously. 
'''

def sanitize_connections_addresses(): 
        ''' Removes the already diconnected connections and addresses. '''
        for index, conn in enumerate(ALL_CONNECTIONS): 
                try: 
                        conn.send(str.encode(' '))
                        data = conn.recv(1024)
                except Exception: 
                        del ALL_CONNECTIONS[index]
                        del ALL_ADDRESSES[index]
                        continue

def list_all_connections():
    """Lists all the connections currently connected to the server."""

    # remove the disconnected connections and addresses
    sanitize_connections_addresses()

    # print the IP and the port of the connection. 
    print('-------Clients------')
    for index, conn in enumerate(ALL_CONNECTIONS):
        print(index, " ", ALL_ADDRESSES[index][0], ":", ALL_ADDRESSES[index][1])


def list_all_addresses():
    """Lists all the addresses currently connected to the server."""

    # remove the disconnected connections and addresses
    sanitize_connections_addresses()

    print("-------Clients------")
    for index, addr in enumerate(ALL_ADDRESSES):
        print(index, " ", addr[0], ":", addr[1])


def parse_command(command):
        ''' Parses the command and takes the index from it to return the socket connection object. '''
        try: 
                target = int(command.replace('select ', ''))
                conn = ALL_CONNECTIONS[target]
                IP = ALL_ADDRESSES[target][0]
                PORT =  ALL_ADDRESSES[target][1]
                logging.info('Connection Successful: {}:{}'.format(IP, PORT))
                # logging.info(str(IP, '> ',))
                print(f'{IP}:{PORT}>', end='')
                return conn, (IP, PORT), target 
        except IndexError: 
                logging.info('Index of socket connection out of bound: {}'.format(target))
        except ValueError: 
                logging.error(
                "Did you forget to pass the command like the format: 'select index' without extra space \
                 and valid index?: {}".format(target)
        )
        except Exception as e: 
                logging.error('Something unexpected happened: {}'.format(str(e)))
        return None, None, None 


# sock is taken from server.
def terminal(sock): 
        ''' Interactive terminal to handle all the connections. '''
        logging.info('Welcome to Interactive Terminal! ')
        logging.info("Press 'q' to exit the terminal. ")
        logging.info("Command Style: 'select index' ")
        
        print('terminal>')
        while True: 
                command = input('terminal> ')
                if command == 'q': 
                        # singal the threads to stop 
                        stop_event.set()
                        
                        # close the server connection. 
                        close_connection(sock)
                        break
                elif command == 'listconn':
                        list_all_connections()
                elif command == 'listaddr': 
                        list_all_addresses()
                elif 'select' in command: 
                        conn, addr, socket_index = parse_command(command)
                        if conn is not None: 
                                commands_handler(conn, sock)
                        else: 
                                logging.error(
                                'Connection has been disconnected with connection object at index: {}'.format(socket_index)
                        )
                else: 
                        print('Invalid command: {}'.format(command))
                        logging.error('Invalid command: {}'.format(command))
        logging.info('You may close the terminal.')
       
