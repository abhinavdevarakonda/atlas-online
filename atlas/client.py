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

with open("country_list.txt","r") as list:
    countries = list.readlines()

    for i in range(len(countries)):
        countries[i] = (countries[i].strip()).lower()


def wordCheck(player_country):
    player_country = player_country.lower()
    if player_country in countries:
        return True
    else:
        print(player_country)
        return False

def receive():
    while True:
        try:
            server_msg = client.recv(1024).decode('ascii')
            if server_msg == NAME_REQ:
                client.send(user_name.encode('ascii'))
            elif server_msg == MSG_REQ:

                player_country = input(MSG_REQ)
                if wordCheck(player_country):
                    message = f"[{user_name}]: {player_country}"
                    client.send(message.encode('ascii'))
                else:
                    while wordCheck(player_country)==False:
                        print("invalid. country not in country list.")
                        player_country = input(MSG_REQ)

                    message = f"[{user_name}]: {player_country}"
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