# receiver_zero
Control your computer remotely using Python3. 

**NOTE: THIS SOFTWARE IS NOT AS SECURE AS IT COULD BE. IT NOW INCLUDES AN OPTIONAL SERVER PASSWORD BUT THERE IT STILL DOES NOT IMPLEMENT A SECURITY LAYER. USE CAUTION WHEN OPERATING THIS SOFTWARE ON NETWORKS THAT YOU DO NOT TRUST OR CONTROL.**
## depends on
pyautogui
```
pip install pyautogui
```

## usage
Run ```receiver_zero/main.py``` with something like:
```
python main.py
```
This is your server. It will take incoming commands and execute them on your host machine. 

To test the server, you can run the example ```example/client.py``` with something like:
```
python client.py
```
### commands
receiver_zero uses a very simple syntax for it's commands.

#### typing:
```
t Here is some text to type!
```
#### press:
```
p f6
```
or
```
p down
```
#### hotkeys:
```
h ctrl c
```
The hotkey command can only accept two key values at this time.
#### multiple commands:
To chain together multiple commands simply separate them with ```&&``` for example:
```
p f6&&t https://www.github.com&&p enter
```
These commands will be executed synchronously. 
#### password
If you have chosen at launch to use a server password, you will need to append it to the end of every command or command list. For a single command you would do that like this:
```
p enter#p#<password>
```
With ```<password>``` being replaced by your actual password. 

The password must always be included at the END of the command or command list and anything in the command after the '#p#' sequence will be read as a password. 

When linking multiple commands together, the password must only be included once at the end of the command list:
```
t hello world!&&p enter&&h ctrl c#p#<password>
```
A space after the end of a command or command list is optional but it is a best practice because if the server is running without a password it would understand a command like:
```
t welcome to the machine#p#<password>
```
As instructing it to type 'welcome to the machine#p#<password>'

A full list of key commands is available here: (also found at http://pyautogui.readthedocs.io/en/latest/keyboard.html)
```
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
```
### todo:
-Add a security layer

-sanitize input