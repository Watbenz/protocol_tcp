from socket import *
from _thread import *
import threading
import game, pickle
import threading

boss_defalut = game.Unit('boss', 200, 500)
boss = boss_defalut.copy()
player = game.Unit('player', 100, 300)
who_attack = []


def threaded(connection_socket):
    global boss, boss_defalut, player, who_attack

    item = game.GameObject(boss.to_string(), 'Unit')

    while True:
        # At first send boss health to client
        # After that send else information to client
        sending_data = pickle.dumps(item)
        connection_socket.send(sending_data)

        # If item turn to be 'END' end this thread
        if item.item == 'END':
            connection_socket.close()
            break

        # Receive input from client
        data = connection_socket.recv(2048).decode()

        # If boss is not died, client can attack
        if boss.status != 'died':
            if data == 'A':
                who_attack.clear()
                who_attack.append(connection_socket)
                player.attack(boss)
                item = game.GameObject('you attack -> ' + boss.to_string(), 'Unit')
            elif data == 'C':
                info = ('name: %s\natk: %d\nhp: %d/%d' % (player.name, player.atk, player.hp, player.MAX_HP))
                item = game.GameObject(info, 'Unit')
            elif data == 'Q':
                item = game.GameObject('END', 'Action')
            else:
                extra = 'other attak -> ' if connection_socket not in who_attack else ''
                item = game.GameObject(extra + boss.to_string(), 'Unit')

        # If boss already died, from attack above, ask client to play again
        if boss.status == 'died':
            item = game.GameObject('Boss has already died\nTry Again? Y: Yes, N: No', 'String')
            if data == 'Y':
                boss = boss_defalut.copy()
                item = game.GameObject(boss.to_string(), 'Unit')
            elif data == 'N':
                item = game.GameObject('END', 'Action')


def main():
    server_name = 'localhost'
    serverPort = 12000

    connections = []

    # welcoming socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((server_name, serverPort))
    server_socket.listen(5)

    print("The server is ready to receive")

    while True:
        connection_socket, addr = server_socket.accept()
        print('Connection From: ' + str(addr))
        threading.Thread(target=threaded, args=(connection_socket,)).start()

    # server_socket.close()


if __name__ == '__main__':
    main()
