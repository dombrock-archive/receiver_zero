import socket
import pyautogui

def get_ip_address():#make a test connection to determine our IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print("Server Running on Local IP: "+get_ip_address())

class Server:
  def authenticate(got,server_password):
    authenticated = False
    if "#p#" in got:
      got_split = got.split("#p#")
      got = got_split[0]
      pwd = got_split[1]
    else:
      pwd = "null"
      print("PWD MISSING!")
    #print("PWD: "+pwd) #debug only
    if pwd!=server_password:
      print("PWD INCORRECT!")
    else:
      authenticated = True
    return got, authenticated

  print("Welcome to receiver_zero.")
  server_password = input("Set Password (or leave blank for no password): ")
  print("OK!")
  if server_password != '':
    print("You have set a password! Make sure that all the commands you send end with '#p#<server_password>'")
    print("Note that if stinging together multiple commands, the password must be included only once, at the end of the command string.")
  else:
    print("You have chosen not to set a password. Warning: This is probably not a great idea. I hope you know what you are doing...")

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  s.bind(('0.0.0.0', 3333))

  s.listen(5)
  flag = 0
  print("\nreceiver_zero is ready to rock!")
  while True:
    auth = False
    if server_password == '':
      auth = True#skip all auth
    connect, addr = s.accept()
    print("Connection Address:" + str(addr))
    str_recv, temp = connect.recvfrom(1024)
    got = str(str_recv.decode("utf-8"))
    print(got)
    #check auth
    if auth != True:
      #skips checking the auth if we are not using a server_password, 
      #because of this, if the user enters a password that is not separated from the command with a space,
      #the password will not be separated from the final command and the command will not be read
      #for example: t test#p#password
      #will type the string 'test#p#password' 
      got, auth = authenticate(got,server_password)
    if auth != True:
      str_return = "Wrong Password"
      connect.sendto(bytes(str_return, 'utf-8'), addr)
      print("closing")
      connect.close()
    #clent has auth
    else:
      str_return = "Received: "+got
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