import socket 


def client(): 
    host = '127.0.0.1'
    port = 15530 

    c = socket.socket()

    c.connect((host, port))

    
    while True: 
        message = input('Input your message to server (q to quit): ')
        if message == 'q': 
            break
        
        c.send(message.encode())
        data = c.recv(1024).decode()

        print('from server: ', data)

    c.close()


if __name__ == '__main__': 
    client()




