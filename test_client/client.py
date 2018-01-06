import socket

while True:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect(("localhost", 3333))#change 'localhost' to your server IP

	str_send = input("cmd: ")

	s.send(bytes(str_send, 'utf-8'))

	str_recv = s.recv(1024)

	print(str(str_recv))
	s.close()