from socket import *
from threading import *

addr = (host, port)
def testFunc():
	while True:
		try:
			data_in = sock.recv(1024)
			data_out = data_in.decode()
			print(data_out)
		except:
			break

try:
	sock = socket()
	host = input("Введите имя хоста: ")
	port = int(input("Введите номер порта: "))
	sock.connect(addr)
except:
	host = "localhost"
	port = 9090
	sock.connect(addr)

password = input("Введите пароль: ")
data_out = password
sock.send(data_out.encode())
testVar = Thread(target = testFunc)
testVar.start()

while data_out != "exit":
	data_out = input()
	if data_out != "exit":
		sock.send(data_out.encode())

data_out = "client disconnected"
sock.send(data_out.encode())
data_in = sock.recv(1024)
sock.close()