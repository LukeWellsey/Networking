import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# send a message to clients connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)

#when client connects to server, recieve inbound message and send any outbound
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            #if client failed, get index and remove it/close connection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send.send('connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server is listening...")
recieve()