"""
Controls the actions on the host machine
Allows the server to control the host machine with pyautogui
"""
import pyautogui
class Input(object):
	def PressKey(inp):
	    print("UNDERSTOOD AS>> press "+inp[1])
	    pyautogui.press(inp[1])

	def TypeString(inp):
		print("UNDERSTOOD AS>> typewrite "+(" ").join(inp[1:]))
		pyautogui.typewrite((" ").join(inp[1:]))

	def HotKey(inp):
	    try:
	      inp[1]
	    except NameError:
	      print("MISSING SECOND HOTKEY!!!")
	    else:
	      print("UNDERSTOOD AS>> hotkey "+inp[1]+", "+inp[2])
	      pyautogui.hotkey(inp[1],inp[2])

	def GoToAddress(inp):
	    print("UNDERSTOOD AS>> go to "+inp[1])
	    pyautogui.hotkey("f6");
	    pyautogui.typewrite(inp[1]);
	    pyautogui.press("enter");    