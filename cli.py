import socket

while True:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect(("localhost", 3333))

	#str_recv = s.recv(1024)

	#print(str(str_recv))

	str_send = input("cmd: ")

	s.send(bytes(str_send, 'utf-8'))

	#str_recv = s.recv(1024)

	#print(str(str_recv))
	s.close()