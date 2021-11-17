from socket import *
import threading
import getpass

def dataOut(sock, data):
    length = str(len(data))
    length = '0' * (9 - len(length)) + length
    data = (length + data).encode()
    sock.send(data)

def dataIn(sock):
    length = sock.recv(9).decode()
    if not length:
        return '', -1
    length = int(length)
    data = sock.recv(length).decode()
    password = data.find('$$$~')
    login = data.find('@$$~')
    result = data.find('@$@~')
    if password != -1:
        return data[4:], 0
    elif login != -1:
        return data[4:], 1
    elif result != -1:
        return data[4:], 2
    else:
        return data, 3

socket.dataOut = dataOut
socket.dataIn = dataIn

def listening(sock):
    while True:
        data = sock.dataIn()
        print(data[0])

def main(sock):
    try:
        while True:
            data = sock.dataIn()
            if data[1] == -1:
                return
            elif data[1] == 1:
                print(data[0])
                sock.dataOut(input())
            elif data[1] == 0:
                print(data[0])
                sock.dataOut(getpass.getpass())
            elif data[1] == 2:
                print(data[0])
                break
            elif data[1] == 3:
                print(data[0])
        print(r'$~: For exit enter "/exit"!')
        threading.Thread(target=listening, args=[sock], daemon=True).start()
        while True:
            for_server = input()
            if for_server == r'/exit':
                break
            sock.dataOut(for_server)
    except (ConnectionAbortedError, ConnectionResetError) as err:
        print(err)

sock = socket()
sock.setblocking(True)
ipAddr = '192.168.1.39'
connPort = 13131
sock.connect((ipAddr, connPort))

main(sock)
sock.close()