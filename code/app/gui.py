import tkinter as tk
import tkinter.messagebox
from subprocess import Popen, PIPE, STDOUT
import server
from multiprocessing import Pool
import time
import pickle
class AppGUI:
	def __init__(self, master):
		self.status_cache = "null"
		self.dump_status("null")
		print("new window")
		master.minsize(width=666, height=20)
		master.maxsize(width=666, height=420)

		self.master = master
		self.readout_text = tk.StringVar()
		self.readout_text.set("start")
		master.title("rz")
		master.bind("<Configure>", self.drag_window)

		self.label = tk.Label(master, text="PRESS START", fg="white", bg="black",padx=100,pady=20)
		self.label.pack(fill='x')

		self.greet_button = tk.Button(master, text="Start", command=self.StartServer)
		self.greet_button.pack(fill='x')

		self.close_button = tk.Button(master, text="Close", command=master.quit)
		self.close_button.pack(fill='x')

		self.lock_ui = False

	def dump_status(self, new_status):
		self.status_cache = pickle.load( open( "com.p", "rb" ) )
		status= new_status
		pickle.dump( status, open( "com.p", "wb" ) )

	def drag_window(self,x):#makes sure the GUI does not update while the window is being dragged		
		if(self.lock_ui == False):
			print("lock gui")
			self.lock_ui = True
			self.master.after(250, self.stop_dragging)

	def stop_dragging(self):
		if(self.lock_ui == True):
			print("unlock gui")
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
		print("beep")
		data = pickle.load( open( "com.p", "rb" ) )
		
		#CHECK STATUS
		data = data.split(",")
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

if __name__ == '__main__':
	root = tk.Tk()
	root.configure(background='#333')
	my_gui = AppGUI(root)
	root.mainloop()