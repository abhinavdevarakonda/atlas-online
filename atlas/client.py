import socket
import threading
import pickle

host = "10.0.0.17" 
port = 55555
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
NAME_REQ = "NAME_REQ"
MSG_REQ = "your turn: "

user_name = input("Enter your name: ")

def receive():
    while True:
        try:
            server_msg = client.recv(1024).decode('ascii')
            if server_msg == NAME_REQ:
                client.send(user_name.encode('ascii'))
            elif server_msg == MSG_REQ:
                message = f"[{user_name}]: {input(MSG_REQ)}"
                client.send(message.encode('ascii'))
            else:
                print(server_msg)

        except:
            print("error")
            client.close()
            break

def send():
    while True:
        message = f"[{user_name}]: {input('')}"
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

#send_thread = threading.Thread(target=send)
#send_thread.start()