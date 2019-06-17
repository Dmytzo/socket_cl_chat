import socket
import select
import sys


HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        
    except Exception as e:
        print(f'error - {e}', file=sys.stderr)

    else:
        if len(message_header):
            message_lenght = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': client_socket.recv(message_lenght)}

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])
        
    for read_socket in read_sockets:
        if read_socket == server_socket:
            client_socket, client_addr = server_socket.accept()

            user = receive_message(client_socket)

            if user:
                sockets_list.append(client_socket)
                clients[client_socket] = user

                print(f"{user['data'].decode('utf-8')} - {client_addr[0]}:{client_addr[1]}")

        else:
            message = receive_message(read_socket)

            if not message:
                print(f"close - {clients[read_socket]['data'].decode('utf-8')}")
                sockets_list.remove(read_socket)
                del clients[read_socket]
                continue

            user = clients[read_socket]
            print(f"{user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != read_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    
