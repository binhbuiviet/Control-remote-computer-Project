from tkinter import*
import os 
import sys

from PIL import Image, ImageTk 

def path(file_name):
    file_name = 'pic\\' + file_name
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".") 
    return os.path.join(base_path, file_name) 

class Homescreen_UI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure(
            bg = "#ff0000",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        parent.geometry("1280x720+200+200")
        self.grid(row=0, column=0, sticky="nsew")
        
        #backround
        self.back_gound_image = ImageTk.PhotoImage(Image.open(path("bg2.jpg")))
        self.back_gound_label = Label(self, image=self.back_gound_image, bg='black')
        self.back_gound_label.pack(fill=X)

        # button - app control
        self.button_app_control = Button(
            self,
            text="App Control",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_app_control.place(
            x=110,
            y=80,
            width=300,
            height=60
        )

        # button - file control
        self.button_file_control = Button(
            self,
            text="File Control",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_file_control.place(
            x=470,
            y=80,
            width=300,
            height=60
        )

        # button - keyboard 
        self.button_keyboard = Button(
            self,
            text="Keyboard",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_keyboard.place(
            x=830,
            y=80,
            width=300,
            height=60
        )
        # button - live creen
        self.button_livescreen = Button(
            self,
            text="Live Screen",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_livescreen.place(
            x=110,
            y=190,
            width=300,
            height=60
        )

        #button - mouse control
        self.button_mouse_control = Button(
            self,
            text="Mouse Control",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_mouse_control.place(
            x=470,
            y=190,
            width=300,
            height=60
        )

        # button - multi task
        self.button_multi_task = Button(
            self,
            text="Multi Task",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_multi_task.place(
            x=830,
            y=190,
            width=300,
            height=60
        )

        self.button_process_control = Button(
            self,
            text="Process Control",
            bg='#363636',
            fg= 'dodgerblue',
            font='helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_process_control.place(
            x=110,
            y=300,
            width=300,
            height=60
        )
        
        # button - screenshot
        self.button_screenshot = Button(
            self,
            text="Screenshot",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_screenshot.place(
            x=470,
            y=300,
            width=300,
            height=60
        )
         #button - shut down
        self.button_shut_down = Button(
            self,
            text="Shut Down",
            bg='#363636',
            fg= 'dodgerblue',
            font='Helvetica 20 bold',
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_shut_down.place(
            x=830,
            y=300,
            width=300,
            height=60
        )

        self.button_disconnect = Button(
            self,
            text="DISCONNECT",
            fg='deeppink', 
            bg='#363636',
            font='Helvetica 24 bold',
            command=lambda: print("button_disconnect clicked"),
            relief="flat"
        )

        self.button_disconnect.place(
            x=470,
            y=440,
            width=300,
            height=60
        )

