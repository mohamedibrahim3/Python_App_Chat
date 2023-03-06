#! python3

import socket
import threading

def handle_client_connection(conn, addr):
    # recieve the client's name
    name = conn.recv(1024).decode().strip()

    # add client to list of clients
    clients.append((conn, addr, name))

    while True:
        # receive data from client
        data = conn.recv(1024).decode()
        if not data:
            break
        
        print(f'{name}: {data}')
        
        # send data to all clients except sender
        for client_conn, client_addr, client_name in clients:
            if client_conn is not conn:
                client_conn.sendall(f'{name}@"{addr[0]}: {addr[1]}": {data}'.encode())
        
        # close the connection if client sends 'bye'
        if data.lower() == 'bye':
            print(f'Closing connection with client {name} ({addr})')
            conn.close()
            clients.remove((conn, addr, name))
            break


# create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# specify a port for client to connect
port = 5000

# bind the socket to a public host and port
server_socket.bind((host, port))

# listen for incoming connections
server_socket.listen()

print('Waiting for clients to connect...')

# list of connected clients
clients = []

while True:
    # wait for a connection
    conn, addr = server_socket.accept()
    print(f'Connection established with client {addr}')

    # handle each client connection in a separate thread
    threading.Thread(target=handle_client_connection, args=(conn, addr)).start()