import threading
import socket
import pickle

host = "127.0.0.1"
port = 55555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(2)
NAME_REQ = "NAME_REQ"
turns = 0
clients,names = [],[]

def broadcast(msg):
    for client in clients:
        client.send(msg) 


def handle(client):
    turns = 0
    while True:
        try:
            if turns%2==0:
                clients[0].send("your turn: ".encode('ascii'))
                msg = clients[0].recv(1024)
                broadcast(msg)
            else:
                clients[1].send("your turn: ".encode('ascii'))
                msg = clients[1].recv(1024)
                broadcast(msg)
            
            turns+=1

        except:
            index = clients.index(client)
            name = names[index]
            names.remove(nickname)
            clients.remove(index)
            client.close()
            broadcast(f"{name} has left the chat".encode('ascii'))
            break


def receive():
    while True:
        client,addr = server.accept()
        print(f"CONNECTED WITH [{str(addr)}]")

        client.send(NAME_REQ.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        print(f"{name} has entered the chat")
        broadcast(f"[{name}] JOINED THE CHAT".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print(f"LISTENING ON {server}")
receive()