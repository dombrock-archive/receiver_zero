import tkinter as tk
import tkinter.messagebox
from subprocess import Popen, PIPE, STDOUT
import server
from multiprocessing import Pool
import time
import pickle
import webbrowser
class AppGUI:
	def __init__(self, master):
		self.status_cache = "null"#dont think this is used still
		self.lock_ui = False
		self.dump_status("null")
		#print("new window")
		master.minsize(width=420, height=50)
		master.maxsize(width=420, height=420)
		master.title("receiver_zero")
		master.bind("<Configure>", self.drag_window)

		self.master = master#what is the point of this?

		self.blinker = tk.Canvas(master,
			height=10,
			bd=0, 
			relief='ridge',
			highlightthickness=0,
			bg="purple")
		self.blinker.pack(fill='x')

		self.label = tk.Label(master, 
			text="PRESS START", 
			fg="white", 
			bg="black",
			padx=100,
			pady=20,
			font=("Arial Black", 10, "bold")
		)
		self.label.pack(fill='x')

		self.connection_label = tk.Label(master, 
			text="Connection\nInfo", 
			fg="white", 
			bg="#333",
			padx=100,
			pady=20,
			font=("Arial Black", 10, "bold")
		)
		self.connection_label.pack(fill='x')

		self.greet_button = tk.Button(master, 
			text="Start", 
			fg="white", 
			bg="#333",
			font=("Arial Black", 10, "bold"),
			command=self.StartServer
		)
		self.greet_button.pack(fill='x')

		self.settings_button = tk.Button(master, 
			text="Settings",
			fg="white", 
			bg="#333", 
			font=("Arial Black", 10, "bold"),
			command=self.settings_window
		)
		self.settings_button.pack(fill='x')

		self.help_button = tk.Button(master, 
			text="Help",
			fg="white", 
			bg="#333", 
			font=("Arial Black", 10, "bold"),
			command=self.help_window
		)
		self.help_button.pack(fill='x')

		self.close_button = tk.Button(master, 
			text="Close",
			fg="white", 
			bg="#333", 
			font=("Arial Black", 10, "bold"),
			command=master.quit
		)
		self.close_button.pack(fill='x')


		
	def settings_window(self):
		#self.master.withdraw()
		self.newWindow = tk.Toplevel(self.master)
		bb = SettingsWindow(self.newWindow)

	def help_window(self):
		webbrowser.open_new("http://www.google.com")

	def dump_status(self, new_status):
		self.status_cache = pickle.load( open( "com.p", "rb" ) )
		status= new_status
		pickle.dump( status, open( "com.p", "wb" ) )
	def dump_connection(self, new_connection):
	    connection= new_connection
	    pickle.dump( connection, open( "connection.p", "wb" ) )


	def drag_window(self,x):#makes sure the GUI does not update while the window is being dragged		
		if(self.lock_ui == False):
			#print("lock gui")
			self.lock_ui = True
			self.master.after(250, self.stop_dragging)

	def stop_dragging(self):
		if(self.lock_ui == True):
			#print("unlock gui")
			self.lock_ui = False

	def SaveWhitelist(self,new):
	    whitefile = open("whitelist.txt", "a")
	    saveData = new+"\n"
	    whitefile.write(saveData)
	    print("updated whitelist with: "+new)

	def update_label(self):
		self.master.after(1000, self.update_label)
		if(self.lock_ui == True):
			return
		#print("beep")
		self.blink()
		data = pickle.load( open( "com.p", "rb" ) )
		con = pickle.load( open( "connection.p", "rb" ) )
		#CHECK STATUS
		data = data.split(",")
		con = con.split(",")
		if(con[0]=="connection"):
			text = "IP: "+con[1]+" \nPORT: "+con[2]
			self.connection_label.config(text=text)
			self.dump_connection("clear")

		if(data[0]=="unknown device"):
			self.dump_status("clear")
			text = "UNKNOWN DEVICE: "+data[1]
			self.label.config(text=text)
			if tk.messagebox.askyesno("Add Device", "Add "+data[1]+" to whitelist?"):
				text = "VERIFIED: "+data[1]
				self.SaveWhitelist(data[1])
				self.label.config(text=text)
			else:
				text = "REFUSED: "+data[1]
				self.label.config(text=text)
		if(data[0]=="waiting"):
			self.dump_status("clear")
			self.label.config(text="Waiting for command...")
		if(data[0]=="got"):
			self.dump_status("clear")
			self.label.config(text=data[1])
		self.master.after(250, self.unblink)


	def blink(self):
		self.blinker.config(bg="limegreen")

	def unblink(self):
		self.blinker.config(bg="skyblue")

	def StartServer(self):
		print("Starting Server")
		self.greet_button.config(text="running")
		self.greet_button.config(state="disabled")
		self.label.config(text="testing")
		#if __name__ == '__main__':
		self.serv = server.Server()
		#serv.StartServer()
		pool = Pool(processes=1)              # Start a worker processes.
		pool.apply_async(self.serv.StartServer)
		self.update_label()

		#self.label.config(text="text")
		
		
		
	def ServerReady(self):
		print("server ready")

class SettingsWindow():
	
	def __init__(self, master):
		self.master = master
		master.minsize(width=420, height=420)
		master.maxsize(width=666, height=666)
		master.title("r_z - Settings")
		master.configure(background="#333")

		self.frame = tk.Frame(self.master)
		self.frame.pack(fill="x")

		self.settings_label = tk.Label(self.master,
			text="SETTINGS",
			fg="white", 
			bg="purple"
		)
		self.settings_label.pack(fill="x")

		self.port_label = tk.Label(self.master,
			text="PORT:",
			fg="white", 
			bg="#333"
		)
		self.port_label.pack(fill="x")
		self.port = tk.Entry(self.master,
			fg="white", 
			bg="dimgrey"
		)
		self.port.pack(fill="x")

		self.save = tk.Button(self.master, 
			text="Save", 
			fg="white", 
			bg="#333",
			command=self.save
		)
		self.save.pack(fill="x")
		#LOAD AND APPLY CONFIG
		self.config_options = self.load()
		self.port.delete(0, len(self.port.get()))
		self.port.insert(0,self.config_options["port"])
		
		
	def load(self):#same as server load function
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


	def save(self):
		port_num = self.port.get()
		self.config_options["port"] = port_num
		configfile = open("config.txt", "w")
		newData = ""
		for option,value in self.config_options.items():
			newData += option+" "+value+"\n"
		print(newData)
		configfile.write(newData)

if __name__ == '__main__':
	root = tk.Tk()
	root.configure(background='#333')
	my_gui = AppGUI(root)
	root.mainloop()


