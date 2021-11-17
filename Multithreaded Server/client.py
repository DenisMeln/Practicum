from socket import *
sock = socket()
sock.setblocking(1)
sock.connect(('192.168.1.39', 9090))

while True:
    msg = input('Введите сообщение: ')
    sock.send(msg.encode())
    if msg == 'exit':
        break
    data = sock.recv(1024)
    print(f'accepted from server:$ {data.decode()}')

sock.close()