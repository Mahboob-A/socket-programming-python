import socket 
import sys 


def create_socket(): 
        ''' Create a socket object '''
        try: 
                global host
                global port 
                global s 
                
                host = ''
                port = 12345
                
                s = socket.socket()
                print('socket creation successful!\n')
                
        except socket.error as err: 
                print('Socket creation error - ', err)

def bind_socket(): 
        ''' Bind to host and port '''
        try: 
                global host 
                global port 
                global s 
                
                s.bind((host, port))
                
                # listening to at most 2 connections 
                s.listen(2)
                print(f"server is listening in host - {'open-to-all' if host == '' else host} and port - {port}")
                
        except socket.error as err: 
                print('Socket binding error - ', err, '\n', 'Reconnecting...')
                bind_socket()

def accept_socket(): 
        ''' Accept the connection '''
        try: 
                global host 
                global port 
                global s 

                conn, addr = s.accept()

                print(f"Connected to address - {addr[0]} and port - {addr[1]}")

                # send commands. passing connection and socket object 
                send_commands(conn, s)
                
                # close the connection and socket after the commads are sent 
                conn.close()
                s.close()


        except socket.error as err:
                print("Error accepting the connection - ", err)


def send_commands(conn, s): 
        ''' Send commands to clinet '''
        
        print("Send Commands to Client... ")

        while True:
                inp = input("Enter command ('q' to exit)...   ")
                if inp == "q":
                        conn.close()
                        s.close()
                        # close the terminal
                        sys.exit()

                encoded_inp = inp.encode()

                if len(encoded_inp) > 0:
                        conn.send(encoded_inp)
                        data = str(conn.recv(1024), 'utf-8')  # same as decoding decode() takes 'utf-8' by default data = conn.recv(1024).decode()
                        print(data, end=" ")


def main(): 
        print('Starting Socket...')
        create_socket()
        bind_socket()
        accept_socket()


# calling main function
main()
