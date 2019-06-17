import errno
import socket
import select
import sys


HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

my_username = input('username: ')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

encoded_username = my_username.encode('utf-8')
encoded_username_header = f'{len(encoded_username):<{HEADER_LENGTH}}'.encode('utf-8')

client_socket.send(encoded_username_header + encoded_username)

while True:
    message = input(f'{my_username} > ')

    if message:
        encoded_message = message.encode('utf-8')
        encoded_message_header = f'{len(encoded_message):<{HEADER_LENGTH}}'.encode('utf-8')
        client_socket.send(encoded_message_header + encoded_message)

    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            
            if not len(username_header):
                print('close')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8').strip()

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')

    except IOError as e:
        if e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):
            print(f'reading error - {e}', file=sys.stderr)
            sys.exit()
        continue

    except Exception as e:
        print(f'error - {e}', file=sys.stderr)
        sys.exit()

