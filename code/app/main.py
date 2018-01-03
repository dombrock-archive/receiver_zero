import socket
import pyautogui


def get_ip_address():#make a test connection to determine our IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print("Server Running on Local IP: ")
print("////////////////////////////")
print("///"+get_ip_address()+"///")
print("////////////////////////////")


class Server:

  def LoadWhitelist(whitelist):
    print("Loading whitelist...")
    whitefile = open("whitelist.txt", "r")
    whitefile = whitefile.read()
    whitefile = whitefile.split("\n")
    for IP in whitefile:
      if "." in IP and IP != "0.0.0.0":
        whitelist.append(IP)
    print(whitelist)
    print("Finished loading whitelist.")
    return whitelist

  def SaveWhitelist(whitelist):
    whitefile = open("whitelist.txt", "w")
    saveData = ""
    for IP in whitelist:
      if "." in IP:
        saveData += IP+"\n"
    whitefile.write(saveData)

  def ReturnData(data,connect,addr,dontclose=False):
    str_return = data
    connect.sendto(bytes(str_return, 'utf-8'), addr)
    connect.close()

  def GetData(connect):
    str_recv, temp = connect.recvfrom(1024)
    got = str(str_recv.decode("utf-8"))
    print("GOT COMMAND>> "+got)
    return got

  def InitSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 3333))
    s.listen(5)
    return s

  def PressKey(inp):
    print("press "+inp[1])
    pyautogui.press(inp[1])

  def TypeString(inp):
    print("typewrite "+(" ").join(inp[1:]))
    pyautogui.typewrite((" ").join(inp[1:]))

  def HotKey(inp):
    try:
      inp[1]
    except NameError:
      print("MISSING SECOND HOTKEY!!!")
    else:
      print("hotkey "+inp[1]+", "+inp[2])
      print("cmd1 "+inp[1]+" cmd2 "+inp[2])
      pyautogui.hotkey(inp[1],inp[2])

  def GoToAddress(inp):
    print("go to "+inp[1])
    pyautogui.hotkey("f6");
    pyautogui.typewrite(inp[1]);
    pyautogui.press("enter");    

  whitelist = ["0.0.0.0"]
  whitelist = LoadWhitelist(whitelist)

  s = InitSocket()

  #flag = 0
  print("  _ _ ___ __ ___(_)_ _____ _ _ ")
  print(" | '_/ -_) _/ -_) \ V / -_) '_|")
  print(" |_| \___\__\___|_|\_/\___|_|  ")
  print("  ______ _ _ ___ ")
  print(" |_ / -_) '_/ _ \ ")
  print(" /__\___|_| \___/")
  print("///////////////////////////////")
  print("RECIVER_ZERO - SERVER IS ONLINE")
  print("///////////////////////////////")


  while True:#MAIN PROGRAM LOOOP
    connect, addr = s.accept()
    connecting_IP = str(addr).split("'")
    connecting_IP = connecting_IP[1]
    print("Connection Address:" + connecting_IP)

    if (connecting_IP in whitelist):#VERIFIED
      got = GetData(connect)
      commands = got.split("&&")
      for inp in commands:
        inp = inp.split(" ")#split into individual commands
        print(inp[0])
        if inp[0] == 'p' or inp[0] == 'P' or inp[0] == 'press' or inp[0] == 'PRESS':#PRESS SINGLE KEY
          PressKey(inp)
        if inp[0] == 't' or inp[0] == 'T' or inp[0] == 'type' or inp[0] == 'TYPE':#TYPE A STRING
          TypeString(inp)
        if inp[0] == 'h' or inp[0] == 'H' or inp[0] == 'hotkey' or inp[0] == 'HOTKEY':#PRESS HOTKEY COMBO
          HotKey(inp)
        if inp[0] == 'g' or inp[0] == 'G' or inp[0] == 'gotoaddr' or inp[0] == 'GOTOADDR':#GO TO WEB ADDRESS (BROWSER ONLY)
          GoToAddress(inp)
        if inp[0] == 'q' or inp[0] == 'Q' or inp[0] == 'quit' or inp[0] == 'QUIT':
          print("should quit now")
          quit()
      ReturnData(got,connect,addr)
    else:#UNVERIFIED
      ReturnData("UNKNOWN DEVICE. CHECK SERVER SOFTWARE.",connect,addr)
      verify = input("Would you like to white list this address? (Type YES to approve)")
      verify = verify.lower()
      print(verify)
      if(verify == "yes"):
        print("Added "+connecting_IP+" to whitelist.")
        whitelist.append(connecting_IP)
        print(whitelist)
        print("Connection to this device is now available.")
        SaveWhitelist(whitelist)
      else:
        print("ACCESS DENIED FOR: "+connecting_IP)
        print("If this was a mistake please try again.")

    
    
