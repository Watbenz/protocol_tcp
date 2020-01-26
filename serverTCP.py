from socket import *
from _thread import *
import threading
import game, pickle


def main():
    boss = None
    player = game.Unit(200, 200)

    server_name = 'localhost'
    serverPort = 12000

    connections = []

    # welcoming socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((server_name, serverPort))
    server_socket.listen(5)

    print("The server is ready to receive")

    while True:
        if not connections:
            connection_socket, addr = server_socket.accept()
            print('Connection From: ' + str(addr))
            connections.append(connection_socket)
            boss = game.Unit(200, 500)
            item = game.GameObject(boss, 'Unit')
        else:
            sending_data = pickle.dumps(item)
            connection_socket.send(sending_data)

            if item.item == 'END':
                connection_socket.close()
                connections.clear()
                continue

            data = connection_socket.recv(2048).decode()

            if boss.status != 'died':
                if data == 'A':
                    player.attack(boss)
                    item = game.GameObject(boss, 'Unit')
                elif data == 'Q':
                    item = game.GameObject('END', 'Action')

            if boss.status == 'died':
                item = game.GameObject('Boss has already died\nTry Again? Y: Yes, N: No', 'String')
                if data == 'Y':
                    boss = game.Unit(50, 300)
                    item = game.GameObject(boss, 'Unit')
                elif data == 'N':
                    item = game.GameObject('END', 'Action')


            # sending_data = pickle.dumps(item)
            # connection_socket.send(sending_data)


    # server_socket.close()


if __name__ == '__main__':
    main()
