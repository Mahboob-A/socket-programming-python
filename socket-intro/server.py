import socket 


def server(): 
    try: 
        host = '127.0.0.1'
        port = 15530 

        s = socket.socket()

        s.bind((host, port))

        s.listen()

        print('server is listening to port: ', port)

        conn, addr = s.accept()

        print("type of conn and addr: ", type(conn), " ", type(addr))
        print('Connected to: ', addr)

        while True: 
            data = conn.recv(1024).decode()

            if not data: 
                break
            print('type of data: ', type(data))
            print('from client: ', data)

            message = input('Input your message: ')

            conn.send(message.encode())
    except Exception as e: 
        print('An error occurred: ', str(e))
    finally:
        conn.close()
        s.close()



if __name__ == '__main__': 
    server()




