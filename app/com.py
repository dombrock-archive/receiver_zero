"""
Handles communication between the server and its multiple data points
*should probably be split into two classes, one for com functions and one for config*
"""

import pickle

class cLayer(object):
	def dump_status(new_status):
		status= new_status
		pickle.dump( status, open( "com/com.p", "wb" ) )

	def dump_connection(new_connection):
		connection= new_connection
		pickle.dump( connection, open( "com/connection.p", "wb" ) )

	def SaveWhitelist(new):
		whitefile = open("config/whitelist.txt", "a")
		saveData = new+"\n"
		whitefile.write(saveData)
		print("updated whitelist with: "+new)

	def LoadWhitelist(whitelist):
		print("Loading whitelist...")
		whitefile = open("config/whitelist.txt", "r")
		whitefile = whitefile.read()
		whitefile = whitefile.split("\n")
		for IP in whitefile:
			if "." in IP and IP != "0.0.0.0":
				whitelist.append(IP)
		print(whitelist)
		print("Finished loading whitelist.")
		self.recheck_whitelist = False
		return whitelist

	def LoadConfig():#copy of GUI load
		config_options = {}
		print("GUI Loading config file...")
		configfile = open("config/config.txt", "r")
		configfile = configfile.read()
		configfile = configfile.split("\n")
		for option in configfile:
			#make sure we are not trying to read a blank line
			if len(option)>0:
				option = option.split( )
				config_options[option[0]] = option[1]
		#print(config_options)#left for easy debug
		return config_options

	def SaveConfig(config_options,port_num):
		config_options["port"] = port_num
		configfile = open("config/config.txt", "w")
		newData = ""
		for option,value in config_options.items():
			newData += option+" "+value+"\n"
		print(newData)
		configfile.write(newData)

	def check_com():
		return pickle.load( open( "com/com.p", "rb" ) )

	def check_con():
		return pickle.load( open( "com/connection.p", "rb" ) )