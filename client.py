import socket
import threading

# create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# specify a port to connect
port = 5000

# connect to the server
client_socket.connect((host, port))

# ask for user's name
# keep asking until user enters a valid name
name = ''

while name == '':
    name = input('Enter your name: ')

client_socket.sendall(name.encode())

# receive messages from server in a separate thread
def receive_messages():
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(data)

threading.Thread(target=receive_messages).start()

# send messages to server
while True:
    message = input('')
    print(f'You: {message}')
    client_socket.sendall(message.encode())
    
    if message.lower() == 'bye':
        print('Closing connection with server...')
        client_socket.close()
        break
