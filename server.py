import threading
import socket

host = '127.0.0.1'##localhost
port = 3000

server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients=[]
nicknames=[]

def broadcast(msg , client_ = ' '):
    for client in clients:
        if client != client_:
            client.send(msg)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message , client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has left the chat".encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client , addr = server.accept()
        print(f"connected with {str(addr)}")
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))
        
        thread = threading.Thread(target=handle , args=(client , ))
        thread.start()

print(f"Listning on the port {port}")
receive()




