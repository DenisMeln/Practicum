from socket import *
from threading import *
from random import *

client_list = []
sock = socket()

def client(conn, addr):
	addrStr = str(addr[0])
	password = conn.recv(128)
	passwordStr = str(password.decode()) + "\n"
	with open("addresses_data.txt", "r", encoding = "utf-8") as fileVar1:
		for i in fileVar1:
			line = i.split(";")
			if addrStr == line[0] and passwordStr == line[1]:
				print("Здравствуйте, ", addr[0])
				break
		else:
			print("Пароль введён неверно, либо Вы - новый пользователь.")
			with open("addresses_data.txt", "a", encoding = "utf-8") as fileVar2:
				fileVar2.write(str(addr[0]) + ";" + str(passwordStr))
			with open("servers_data.txt", "a", encoding = "utf-8") as fileVar3:
				fileVar3.write(str(addr) + " connected\n")
	while True:
		data_in = conn.recv(1024)
		if not data_in:
			break
		data_out = data_in.decode()
		if data_out != "client disconnected":
			print(addr, data_out)
			for user in client_list:
				if conn != user:
					dataVar = str(addr) + str(data_out)
					user.send(dataVar.encode())
		else:
			with open("servers_data.txt", "a", encoding = "utf-8") as fileVar4:
				fileVar4.write(str(addr) + " disconnected\n")
				try:
					client_list.remove(conn)
				except:
					break
	conn.close()
	
try:
	port = 9090
	sock.bind(("", port))
except:
	port = random.randint(1024, 65535)
	sock.bind(("", port))
	
sock.listen(0)
print("Номер порта: ", port)
data_out = ""

while True:
	conn, addr = sock.accept()
	client_list.append(conn)
	client = Thread(target = client, args = (conn, addr))
	client.start()