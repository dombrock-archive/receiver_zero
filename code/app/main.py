import socket
import pyautogui

class Server(object):
  def get_ip_address(self):#make a test connection to determine our IP
    ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ts.connect(("8.8.8.8", 80))
    return_data = ts.getsockname()[0]
    ts.close()
    return return_data

  def clear_screen(self):
    print('\n'*512)

  def ReadyServer(self,config_options):
    print("\n\nServer Running on Local IP: ")
    print("////////////////////////////")
    print(">>>"+self.get_ip_address()+"<<<")
    print("Server Running on Port: ")
    print(">>>"+config_options['port']+"<<<")
    print("////////////////////////////\n")
    input("Please make sure that receiver_zero is allowed through your firewall and press ENTER to continue.\n\n")
    #wait for enter, this is really to make sure that the server doesn't run until we are sure the firewall is clear


  def ShowWelcomeMessage(self):
    welcomefile = open("welcome_message.txt", "r")
    welcomefile = welcomefile.read()
    welcomefile = welcomefile.split("\n")
    for line in welcomefile:
      print(line)

  def LoadConfig(self):
    config_options = {}
    print("Loading config file...")
    configfile = open("config.txt", "r")
    configfile = configfile.read()
    configfile = configfile.split("\n")
    for option in configfile:
      option = option.split( )
      config_options[option[0]] = option[1]
    #print(config_options)#left for easy debug
    return config_options

  def LoadWhitelist(self,whitelist):
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

  def SaveWhitelist(self,whitelist):
    whitefile = open("whitelist.txt", "w")
    saveData = ""
    for IP in whitelist:
      if "." in IP:
        saveData += IP+"\n"
    whitefile.write(saveData)

  def ReturnData(self,data,connect,addr,dontclose=False):
    str_return = data
    connect.sendto(bytes(str_return, 'utf-8'), addr)
    connect.close()

  def GetData(self,connect):
    str_recv, temp = connect.recvfrom(1024)
    got = str(str_recv.decode("utf-8"))
    print("GOT COMMAND>> "+got)
    return got

  def InitSocket(self,config_options):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', int(config_options["port"])))
    s.listen(5)
    return s

  def PressKey(self,inp):
    print("UNDERSTOOD AS>> press "+inp[1])
    pyautogui.press(inp[1])

  def TypeString(self,inp):
    print("UNDERSTOOD AS>> typewrite "+(" ").join(inp[1:]))
    pyautogui.typewrite((" ").join(inp[1:]))

  def HotKey(self,inp):
    try:
      inp[1]
    except NameError:
      print("MISSING SECOND HOTKEY!!!")
    else:
      print("UNDERSTOOD AS>> hotkey "+inp[1]+", "+inp[2])
      #print("cmd1 "+inp[1]+" cmd2 "+inp[2])#left for debug
      pyautogui.hotkey(inp[1],inp[2])

  def GoToAddress(self,inp):
    print("UNDERSTOOD AS>> go to "+inp[1])
    pyautogui.hotkey("f6");
    pyautogui.typewrite(inp[1]);
    pyautogui.press("enter");    

  def MainLoop(self,s,whitelist,config_options):
     while True:#MAIN PROGRAM LOOOP
        connect, addr = s.accept()
        connecting_IP = str(addr).split("'")
        connecting_IP = connecting_IP[1]
        print("Connection Address:" + connecting_IP)

        if (connecting_IP in whitelist) or config_options["allow_unverified_connections"] == "True":#VERIFIED
          if(config_options["allow_unverified_connections"] == "True"):
            print("\n*WARNING ALLOWING UNVERIFIED CONNECTIONS*\n")
          got = self.GetData(connect)
          commands = got.split("&&")
          for inp in commands:
            inp = inp.split(" ")#split into individual commands
            #print(inp[0])#left for debug
            if inp[0] == 'p' or inp[0] == 'P' or inp[0] == 'press' or inp[0] == 'PRESS':#PRESS SINGLE KEY
              self.PressKey(inp)
            if inp[0] == 't' or inp[0] == 'T' or inp[0] == 'type' or inp[0] == 'TYPE':#TYPE A STRING
              self.TypeString(inp)
            if inp[0] == 'h' or inp[0] == 'H' or inp[0] == 'hotkey' or inp[0] == 'HOTKEY':#PRESS HOTKEY COMBO
              self.HotKey(inp)
            if inp[0] == 'g' or inp[0] == 'G' or inp[0] == 'gotoaddr' or inp[0] == 'GOTOADDR':#GO TO WEB ADDRESS (BROWSER ONLY)
              self.GoToAddress(inp)
            if inp[0] == 'q' or inp[0] == 'Q' or inp[0] == 'quit' or inp[0] == 'QUIT':
              print("should quit now")
              quit()
          self.ReturnData(got,connect,addr)
          print("\n")
        else:#UNVERIFIED
          self.ReturnData("UNKNOWN DEVICE. CHECK SERVER SOFTWARE.",connect,addr)
          verify = input("Would you like to white list this address? (Type YES to approve)\n")
          verify = verify.lower()
          if(verify == "yes"):
            print("Added "+connecting_IP+" to whitelist.")
            whitelist.append(connecting_IP)
            print(whitelist)
            print("Connection to this device is now available.")
            self.SaveWhitelist(whitelist)
          else:
            print("ACCESS DENIED FOR: "+connecting_IP)
            print("If this was a mistake please try again.") 

  def StartServer(self):
    self.clear_screen()
    config_options = self.LoadConfig()

    if config_options["display_welcome_message"] == "True":
      self.ShowWelcomeMessage()

    self.ReadyServer(config_options)

    whitelist = ["0.0.0.0"]
    whitelist = self.LoadWhitelist(whitelist)

    s = self.InitSocket(config_options)
    
    print("\n\nWaiting for command...\n\n")
    self.MainLoop(s,whitelist,config_options)

    

   
    
serv = Server()
serv.StartServer()
