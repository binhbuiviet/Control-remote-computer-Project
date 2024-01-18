import keyboard
import struct
from tkinter import*
from PIL import Image, ImageTk
import threading
import os
import sys

def path(file_name):
    file_name = 'pic\\' + file_name
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)

class Keyboard_UI(Frame):
    def __init__(self, parent, client_socket):    
        Frame.__init__(self, parent)
        self.configure(
            bg = "black",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        parent.geometry("1280x720+200+200")

         #backround
        self.back_gound_image = ImageTk.PhotoImage(Image.open(path("bg3.jpg")))
        self.back_gound_label = Label(self, image=self.back_gound_image, bg='black')
        self.back_gound_label.pack(fill=X)

        self.client = client_socket

        self.text = ""
        self.text_1 = Text(
            self, height=200, width=500, state="normal", wrap="char",
            bd=0, bg='white', highlightthickness=0
        )
        self.text_1.place(x=250, y=120, width=600, height=360)

        self.announce = Label(self, text="Press Esc to Stop", fg='white', bg='dodgerblue', width=60, height=5)
        self.announce.place(x=480, y=60, width=135, height=50)
        

        self.button_process = Button(
            self, text='START', width=20, height=5, fg='white', bg='dodgerblue',
            borderwidth=0, highlightthickness=0, command=self.send_keyboard,font='Helvetica 12 bold', relief="flat"
        )
        self.button_process.place(x = 910, y = 259, width=135, height=50)

        self.grid(row=0, column=0, sticky="nsew")
        self.button_back = Button(
            self, text='BACK', width=20, height=5, fg='white', bg='dodgerblue',
            borderwidth=0, highlightthickness=0,font='Helvetica 12 bold', relief="flat"
        )
        self.button_back.place(x = 910, y = 339, width=135, height=50)
        self.thread = None

    def update_text_content(self, new_text):
        self.text_1.config(state="normal")
        self.text_1.insert("end", new_text)
        self.text_1.insert("end", ' ')
        self.text_1.config(state="disabled")

    def send_keyboard(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.send_keys_thread)
            self.thread.start()

    def send_keys_thread(self):
        while True:
            event = keyboard.read_event()
            key = event.name
            key_event = event.event_type
            # Gửi phím nhấn cho client
            if key == "esc" and key_event == "down":

                self.client.sendall(struct.pack('!I', len(key)))
                self.client.send(key.encode())

                self.client.sendall(struct.pack('!I', len(key_event)))
                self.client.send(key_event.encode())

                print(f"Da gui phim {key} {key_event}")
                break
            else:
            
                self.client.sendall(struct.pack('!I', len(key)))
                self.client.send(key.encode())

                self.client.sendall(struct.pack('!I', len(key_event)))
                self.client.send(key_event.encode())

                if key_event == "down":
                    self.update_text_content(key)
#import os
#import socket
#import pyautogui
#from PIL import ImageGrab
#import struct

#def recv_keyboard(client_socket):
#    while True:
#        # Nhận phím nhấn từ server
#        data1 = client_socket.recv(4)
#        size_of_key = struct.unpack('!I', data1)[0]
#        key = client_socket.recv(size_of_key).decode()

#        data2 = client_socket.recv(4)
#        size_of_key_event = struct.unpack('!I', data2)[0]
#        key_event = client_socket.recv(size_of_key_event).decode()
#        print(f"Da nhan phim {key} {key_event}")

#        # Kiểm tra nếu phím Esc được nhấn thì thoát khỏi vòng lặp
#        if key == "esc" and key_event == "down":
#            break
#        elif key_event == "down":
#            pyautogui.keyDown(key)
#        elif key_event == "up":
#            pyautogui.keyUp(key)


