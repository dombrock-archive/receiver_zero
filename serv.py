import socket
import pyautogui

def get_ip_address():#make a test connection to determine our IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print("Server Running on Local IP: "+get_ip_address())

class Server:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  s.bind(('0.0.0.0', 3333))

  s.listen(5)
  flag = 0
  while True:
    connect, addr = s.accept()
    print("Connection Address:" + str(addr))
    str_recv, temp = connect.recvfrom(1024)
    got = str(str_recv.decode("utf-8"))
    print(got)
    str_return = "Server received:" +"\r\n"+ got 
    connect.sendto(bytes(str_return, 'utf-8'), addr)
    commands = got.split("&&")
    for inp in commands:
      inp = inp.split(" ")#separate into commands
      print(inp[0])
      if inp[0] == 'p':
        print("press "+inp[1])
        pyautogui.press(inp[1])
      if inp[0] == 't':
        print("typewrite "+(" ").join(inp[1:]))
        pyautogui.typewrite((" ").join(inp[1:]))
      if inp[0] == 'h':
        print("hotkey "+inp[1]+", "+inp[2])
        print("cmd1 "+inp[1]+" cmd2 "+inp[2])
        pyautogui.hotkey(inp[1],inp[2])
      if inp[0] == 'g':
        print("go to "+inp[1])
        pyautogui.hotkey("f6");
        pyautogui.typewrite(inp[1]);
        pyautogui.press("enter");
      if inp[0] == 'q':
        print("should quit now")
        quit() 
    print("closing")
    connect.close()

serv = Server()