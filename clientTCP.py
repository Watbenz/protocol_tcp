from socket import *
import pickle


serverName = 'localhost'
serverPort = 12000

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((serverName, serverPort))

running = True
special_message = ''

while running:
    received = client_socket.recv(2048)
    obj = pickle.loads(received)

    if obj.typ == 'Unit':
        print(obj.item)
    elif obj.typ == 'String':
        special_message = obj.item
    elif obj.typ == 'Action':
        if obj.item == 'END':
            break

    if not special_message:
        print('A: Attack, Q: Quit')
    else:
        print(special_message)
        special_message = ''

    data = input('Choose an action: ').upper()
    if not data:
        data = ' '
    client_socket.send(data.encode())

    print('----------------')




print('Game is exit, Thank you')
client_socket.close()

