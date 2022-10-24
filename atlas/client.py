import socket
import threading
import pickle

#10.0.0.17 - ipv4 on pc
#10.0.0.26 - ipv4 on laptop
host = "10.0.0.26" 
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

def extract(word):
    for i in word:
        if i == ' ':
            index = word.index(i)

    extracted_word = word[index+1:]
    print(f"start your word with: {extracted_word[-1]}")
    return extracted_word

def wordCheck(player_country,previous_word):
    player_country = player_country.lower()
    if player_country in countries:
        if previous_word == "":
            return True
        else:
            print(previous_word)
            if player_country[0] == previous_word[-1]:
                return True
            else:
                return False
    else:
        return False

previous_word = ""
def receive():
    while True:
        try:
            server_msg = client.recv(1024).decode('ascii')
            if server_msg == NAME_REQ:
                client.send(user_name.encode('ascii'))
            elif server_msg == MSG_REQ:

                player_country = input(MSG_REQ)
                if wordCheck(player_country,previous_word):
                    message = f"[{user_name}]: {player_country}"
                    client.send(message.encode('ascii'))
                else:
                    while wordCheck(player_country,previous_word)==False:
                        print("invalid. country not in country list.")
                        player_country = input(MSG_REQ)

                    message = f"[{user_name}]: {player_country}"
                    client.send(message.encode('ascii'))
            else:
                if server_msg == "Connected to the server":
                    previous_word = ""
                else:
                    previous_word = extract(server_msg)
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