import socket
import threading

host = "127.0.0.1"
port = 4813

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients_ip = []
nicknames = []

def broadcast(message):
    for client in clients_ip:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients_ip.index(client)
            clients_ip.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left chat!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print("Connected {}".format(str(address)))
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients_ip.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send("Connected to server!".encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server listening...")
receive()