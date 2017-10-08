from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, NumericProperty, ObjectProperty


import socket
from functools import partial


addr = "10.0.0.6"

class MainScreen(Screen):
    

    def callback(root):
        root.label_change = "Changed to change"
    pass

class SettingScreen(Screen):
    global addr
    text = addr
    def connect(root, address):
        global addr
        addr = address
        print("new addr="+addr)

    pass

class DesktopScreen(Screen):
    pass

class MyApp(App):
    connected = "Not Connected"

    def test(root, inp):
        #root.manager.get_screen('main').ids.Connected.text = "x"
        global addr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(addr)
        app= App.get_running_app()
        try: 
            print("connecting to: "+addr)
            s.connect((addr, 3333))
            print("Connectedx")
            app.sm.get_screen('main').ids.Connected.text = "Connected"
            print("fuck")
            str_recv = s.recv(1024)
            print(str(str_recv))
        except OSError as err:
            print("OS error: {0}".format(err))
            app.sm.get_screen('main').ids.Connected.text = "Connection Error!"
            print("NOT Connected")
            return
        #except:
        #    print("err1")
        str_send = inp

        try:
            s.send(bytes(str_send.encode('utf-8')))
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("err2")

        try:
            str_recv = s.recv(1024)
            print(str(str_recv))
            print("close")
            s.close()
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("err3")

    def goTo(root, url):
        print("going to"+url)
        root.test('p f6')
        root.test('t '+url)
        root.test('p enter')
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(SettingScreen(name='settings'))
        self.sm.add_widget(DesktopScreen(name='desktop'))
        return self.sm


if __name__ == '__main__':
    MyApp().run()