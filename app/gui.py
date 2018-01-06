"""
Controls the GUI
Uses multiprocessing to create an instance of the server.py
Interfaces with the server via com.py
"""
import tkinter as tk
import tkinter.messagebox
import multiprocessing
import pickle
import webbrowser
#LOCAL IMPORTS
import server
import cLayer
class AppGUI:
	def __init__(self, master):
		self.status_cache = "null"#dont think this is used still
		self.lock_ui = False
		cLayer.com.dump_status("null")
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

		self.settingsWindow = None


	#MAIN WINDOW FUNCTIONS	
	def settings_window(self):
		self.close_settings_window()#make sure we do not open multiple windows
		self.settingsWindow = tk.Toplevel(self.master)
		self.settingsWindow = SettingsWindow(self.settingsWindow)

	def close_settings_window(self):
		if(self.settingsWindow!=None):
			self.settingsWindow.master.destroy()

	def help_window(self):
		webbrowser.open_new("https://github.com/matdombrock/receiver_zero")

	def drag_window(self,x):#makes sure the GUI does not update while the window is being dragged		
		if(self.lock_ui == False):
			#print("lock gui")
			self.lock_ui = True
			self.master.after(250, self.stop_dragging)

	def stop_dragging(self):
		if(self.lock_ui == True):
			#print("unlock gui")
			self.lock_ui = False

	def update_label(self):
		self.master.after(1000, self.update_label)
		if(self.lock_ui == True):
			return
		#print("beep")
		self.blink()
		data = cLayer.com.check_com()
		con = cLayer.com.check_con()
		#CHECK STATUS
		data = data.split(",")
		con = con.split(",")
		if(con[0]=="connection"):
			text = "IP: "+con[1]+" \nPORT: "+con[2]
			self.connection_label.config(text=text)
			cLayer.com.dump_connection("clear")

		if(data[0]=="unknown device"):
			cLayer.com.dump_status("clear")
			text = "UNKNOWN DEVICE: "+data[1]
			self.label.config(text=text)
			if tk.messagebox.askyesno("Add Device", "Add "+data[1]+" to whitelist?"):
				text = "VERIFIED: "+data[1]
				cLayer.config.SaveWhitelist(data[1])
				self.label.config(text=text)
			else:
				text = "REFUSED: "+data[1]
				self.label.config(text=text)
		if(data[0]=="waiting"):
			cLayer.com.dump_status("clear")
			self.label.config(text="Waiting for command...")
		if(data[0]=="got"):
			cLayer.com.dump_status("clear")
			self.label.config(text=data[1])
		self.master.after(250, self.unblink)


	def blink(self):
		self.blinker.config(bg="limegreen")

	def unblink(self):
		self.blinker.config(bg="skyblue")

	def StartServer(self):
		print("Starting Server")
		self.close_settings_window()
		self.greet_button.config(text="Running")
		self.greet_button.config(state="disabled")
		self.settings_button.config(state="disabled")
		self.label.config(text="testing")
		self.serv = server.Server()

		pool = multiprocessing.Pool(processes=1)
		pool.apply_async(self.serv.StartServer)

		self.update_label()
		
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
			font=("Arial Black", 10, "bold"), 
			bg="purple"
		)
		self.settings_label.pack(fill="x")

		self.port_label = tk.Label(self.master,
			text="PORT:",
			fg="white", 
			font=("Arial Black", 10, "bold"), 
			bg="#333"
		)
		self.port_label.pack(fill="x")
		self.port = tk.Entry(self.master,
			fg="white", 
			bg="dimgrey",
			justify="center",
			font=("Arial Black", 10, "bold")
		)
		self.port.pack(fill="x")

		self.save = tk.Button(self.master, 
			text="Save", 
			fg="white", 
			bg="#333",
			font=("Arial Black", 10, "bold"), 
			command=lambda: cLayer.config.SaveConfig(self.config_options,self.port.get())
		)
		self.save.pack(fill="x")
		#LOAD AND APPLY CONFIG
		self.config_options = cLayer.config.LoadConfig()
		self.port.delete(0, len(self.port.get()))
		self.port.insert(0,self.config_options["port"])

if __name__ == '__main__':
	multiprocessing.freeze_support()#required for pyinstaller
	#https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
	root = tk.Tk()
	root.configure(background='#333')
	my_gui = AppGUI(root)
	root.mainloop()


