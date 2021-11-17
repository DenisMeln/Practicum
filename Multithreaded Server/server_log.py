import socket
import threading
import time
import os
import random
import csv
import hashlib

def dataOut(sock, data, serviceData=''):
    length = str(len(data + serviceData))
    length = '0' * (9 - len(length)) + length
    data = (length + serviceData + data).encode()
    sock.send(data)

def dataIn(sock):
    length = int(sock.recv(9).decode())
    data = sock.recv(length).decode()
    return data

def print_log(*data):
    data = ' '.join((str(el) for el in data))
    global LOCK, LOG, log_file
    if LOG:
        with LOCK:
            print(data)
            with open(log_file, 'a+') as file:
                file.write(data + '\n')

socket.dataOut = dataOut
socket.dataIn = dataIn

def register(conn, addr, file_list):
    global pass_file
    while True:
        conn.dataOut('Create login!', '@$$~')
        login = conn.dataIn()
        for row in file_list:
            if row[1] == login:
                print_log('This login has already userd!')
        else:
            break

    conn.dataOut('Create password!', '$$$~')
    password = conn.dataIn()
    ipAddr = hashlib.md5(addr[0].encode()).hexdigest()
    password = hashlib.md5(password.encode()).hexdigest()
    row = ipAddr, login, password
    with LOCK:
        with open(pass_file, 'a+', newline='') as clients:
            writer = csv.writer(clients, delimiter=';')
            writer.writerow(row)
    conn.dataOut('You have registered')
    print_log(f'{addr[0]} has registered')
    return login, password

def authentification(conn, addr, password, attempts=3):
    global client_list
    if attempts == 0:
        conn.dataOut('You entered invalid password for 3 times')
        return False
    conn.dataOut('Enter your password', '$$$~')
    recv_password = conn.dataIn()
    if password == hashlib.md5(recv_password.encode()).hexdigest():
        conn.dataOut('You are logged on! Let\'s go!', '@$@~')
        print_log(f'{addr[0]} logged on')
        client_list.append(conn)
        return True
    else:
        conn.dataOut('invalid password')
        return authentification(conn, addr, password, attempts - 1)

def listening(conn, addr):
    global client_list, LOCK, pass_file, message_history
    with LOCK:
        with open(pass_file, 'a+', newline='') as clients:
            clients.seek(0, 0)
            reader = csv.reader(clients, delimiter=';')
            file_list = list(reader)
    try:
        for row in file_list:
            if row[0] == hashlib.md5(addr[0].encode()).hexdigest():
                login, password = row[1], row[2]
                break
        else:
            login, password = register(conn, addr, file_list)
        if authentification(conn, addr, password):
            while True:
                data = conn.dataIn()
                with LOCK:
                    with open(message_history, 'a+', newline='') as msg_hst:
                        writer = csv.writer(msg_hst, delimiter=';')
                        writer.writerow((addr[0], login, data))
                data = login + " &~: " + data
                print_log(data)
                conn_list = list(client_list)
                conn_list.remove(conn)
                for clnt_conn in conn_list:
                    clnt_conn.dataOut(data)
        else:
            print_log('Authentification failed!')
            conn.close()
    except (ConnectionAbortedError, ConnectionResetError, ValueError) as err:
        client_list.remove(conn)
        print_log(err, addr[0])
    print_log(f'Connection with {addr[0]} closed!')

def connecting(sock):
    global LOCK, LISTEN
    while True:
        if LISTEN:
            conn, addr = sock.accept()
            print_log(f'Client {addr[0]} has connected!')
            threading.Thread(target=listening, args=(conn, addr), daemon=True).start()

def bind(sock, connPort):
    while True:
        try:
            sock.bind(('', connPort))
            break
        except OSError as oserr:
            print_log("{} (port {} is taken)".format(oserr, connPort))
            connPort = random.randint(1024, 65535)
    sock.listen(0)
    print_log('Server is running at port {}'.format(connPort))

client_list = []
LOCK = threading.Lock()
LISTEN = True
LOG = True
connPort = 13131
pass_file = "clients.csv"
message_history = f'msg_hst_{time.time()}.csv'
log_file = f'log_{time.time()}.txt'
sock = socket.socket()
sock.setblocking(True)
bind(sock, connPort)

threading.Thread(target=connecting, args=(sock,), daemon=True).start()
commands = '''shutdown - to shutdown server
clear file - to clear clients list
stop listen - to stop listen port
start listen - to start listen port
stop log - to stop print log
start log - to start print log
clear log - to clear log file'''
print(commands)

while True:
    cmd = input()
    if cmd == 'shutdown':
        break
    elif cmd == 'clear file':
        with open(pass_file, 'w', newline='') as clients:
            pass
    elif cmd == 'stop listen':
        LISTEN = False
    elif cmd == 'start listen':
        LISTEN = True
    elif cmd == 'stop log':
        LOG = False
    elif cmd == 'start log':
        LOG = True
    elif cmd == 'clear log':
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        with open(log_file, 'w'):
            pass

sock.close()