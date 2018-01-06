import socket
import controls
from multiprocessing import Pool
import asyncio
import pickle
'''
issue with whitelist will be caused from dynamic IPs
possible solution is to only have a live whitelist by default
each time server is run it will need to have the IP approved
option to use a static whitelist file for setups with static IPS
'''
class Server(object):
  def dump_status(self, new_status):
    status= new_status
    pickle.dump( status, open( "com.p", "wb" ) )

  def dump_connection(self, new_connection):
    connection= new_connection
    pickle.dump( connection, open( "connection.p", "wb" ) )

  def get_ip_address(self):#make a test connection to determine our IP
    ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ts.connect(("8.8.8.8", 80))
    return_data = ts.getsockname()[0]
    ts.close()
    return return_data

  def clear_screen(self):
    print('\n'*512)

  def ReadyServer(self,config_options):
    IP = self.get_ip_address()
    print("\n\nServer Running on Local IP: ")
    print("////////////////////////////")
    print(">>>"+IP+"<<<")
    print("Server Running on Port: ")
    print(">>>"+config_options['port']+"<<<")
    print("////////////////////////////\n")
    msg = "connection,"+IP+","+config_options['port']
    self.dump_connection(msg)

  def ShowWelcomeMessage(self):
    welcomefile = open("welcome_message.txt", "r")
    welcomefile = welcomefile.read()
    welcomefile = welcomefile.split("\n")
    for line in welcomefile:
      print(line)

  def LoadConfig(self):#copy of GUI load
    config_options = {}
    print("GUI Loading config file...")
    configfile = open("config.txt", "r")
    configfile = configfile.read()
    configfile = configfile.split("\n")
    for option in configfile:
      #make sure we are not trying to read a blank line
      if len(option)>0:
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
    self.recheck_whitelist = False
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

  def ServerLoop(self,s,whitelist,config_options):
    print("starting server loop")
    while True:#MAIN PROGRAM LOOOP
        print("running server loop")
        
        connect, addr = s.accept()
        connecting_IP = str(addr).split("'")
        connecting_IP = connecting_IP[1]
        msg= "Connection Address:" + connecting_IP
        print(msg)
        self.dump_status(msg)
        if(connecting_IP not in whitelist):
          print("ip no found reloading whitelist")
          whitelist = self.LoadWhitelist(whitelist)
        if (connecting_IP in whitelist) or config_options["allow_unverified_connections"] == "True":#VERIFIED
          if(config_options["allow_unverified_connections"] == "True"):
            print("\n*WARNING ALLOWING UNVERIFIED CONNECTIONS*\n")
          got = self.GetData(connect)
          commands = got.split("&&")
          for inp in commands:
            inp = inp.split(" ")#split into individual commands
            #print(inp[0])#left for debug
            if inp[0] == 'p' or inp[0] == 'P' or inp[0] == 'press' or inp[0] == 'PRESS':#PRESS SINGLE KEY
              controls.Input.PressKey(inp)
            if inp[0] == 't' or inp[0] == 'T' or inp[0] == 'type' or inp[0] == 'TYPE':#TYPE A STRING
              controls.Input.TypeString(inp)
            if inp[0] == 'h' or inp[0] == 'H' or inp[0] == 'hotkey' or inp[0] == 'HOTKEY':#PRESS HOTKEY COMBO
              controls.Input.HotKey(inp)
            if inp[0] == 'g' or inp[0] == 'G' or inp[0] == 'gotoaddr' or inp[0] == 'GOTOADDR':#GO TO WEB ADDRESS (BROWSER ONLY)
              controls.Input.GoToAddress(inp)
            if inp[0] == 'q' or inp[0] == 'Q' or inp[0] == 'quit' or inp[0] == 'QUIT':
              print("should quit now")
              quit()
          self.ReturnData(got,connect,addr)
          self.dump_status("got,"+got)
          print("\n")
        else:#UNVERIFIED
          self.ReturnData("UNKNOWN DEVICE. CHECK SERVER SOFTWARE.",connect,addr)
          self.dump_status("unknown device,"+connecting_IP)
          self.recheck_whitelist = True
          #REMOVED WHITELIST ABILITY FROM SERVER
          '''
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
          '''

  def StartServer(self):
    self.recheck_whitelist =False
    self.dump_status("Starting...")
    self.clear_screen()
    config_options = self.LoadConfig()
    if config_options["display_welcome_message"] == "True":
      self.ShowWelcomeMessage()

    self.ReadyServer(config_options)

    whitelist = ["0.0.0.0"]
    whitelist = self.LoadWhitelist(whitelist)

    s = self.InitSocket(config_options)
    
    print("\n\nWaiting for command...\n\n")
    self.dump_status("waiting")
    #if __name__ == '__main__':
    #pool2 = Pool(processes=1)              # Start a worker processes.
    #pool2.apply_async(self.ServerLoop,[s,whitelist,config_options] ,self.callback) 
    self.ServerLoop(s,whitelist,config_options)
    #loop = asyncio.get_event_loop()

  def callback(self):
    print("callback")
    

    

   
    

