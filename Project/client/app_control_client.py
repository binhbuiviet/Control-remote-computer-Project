import tkinter as tk
from tkinter import  ttk
import pickle, struct
from tkinter import*
from PIL import Image, ImageTk

BUFSIZ = 1024 * 4
import os
import sys
import socket
def path(file_name):
    file_name = 'pic\\' + file_name
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)

def recvall(socket, client_socket):
    message = bytearray()
    while len(message) < client_socket:
        buffer = socket.recv(client_socket - len(message))
        if not buffer:
            raise EOFError('Could not receive all expected data!')
        message.extend(buffer)
    return bytes(message)

def receive(client_socket):
    packed = recvall(client_socket, struct.calcsize('!I'))
    size = struct.unpack('!I', packed)[0]
    data = recvall(client_socket, size)
    return data

def send_kill(client_socket):
    global app_name
    client_socket.sendall(bytes("0", "utf8"))
    client_socket.sendall(bytes(str(app_name.get()), "utf8"))
    message = client_socket.recv(BUFSIZ).decode("utf8")
    if "1" in message:
        tk.messagebox.showinfo(message = "Đã đóng ứng dụng!")
    else:
        tk.messagebox.showerror(message = "Lỗi! Không thể đóng ứng dụng.")
    return

def list_app(client_socket, tab):
    client_socket.sendall(bytes("1", "utf8"))
    list_name = receive(client_socket)
    list_name = pickle.loads(list_name)
    list_id = receive(client_socket)
    list_id = pickle.loads(list_id) 
    list_thread = receive(client_socket)
    list_thread = pickle.loads(list_thread)
    print(list_name)
    print(list_id)
    print(list_thread)
    for i in tab.get_children():
        tab.delete(i)
    for i in range(len(list_name)):
        tab.insert(parent = '', index = 'end', text = '', values = (list_name[i], list_id[i], list_thread[i]))
    return

def clear(tab):
    for i in tab.get_children():
        tab.delete(i)
    return

def send_start(client_socket):
    global app_name
    client_socket.sendall(bytes("3", "utf8"))
    client_socket.sendall(bytes(str(app_name.get()), "utf8"))
    return
        
def start(root, client_socket):
    app_start = tk.Toplevel(root)
    app_start['bg'] = 'black'
    app_start.geometry("420x50")
    global app_name
    app_name = tk.StringVar(app_start)
    tk.Entry(app_start, textvariable = app_name, width = 35, borderwidth = 5).place(x= 8, y= 20)
    tk.Button(app_start, text = "Start", width = 14, height = 2, fg = 'white', bg = 'dodgerblue', borderwidth=0,
            highlightthickness=0, command = lambda: send_start(client_socket), relief="flat").place(x= 300, y= 13)
    return
    
def kill(root, client_socket):
    kill = tk.Toplevel(root)
    kill['bg'] = 'black'
    kill.geometry("420x50")
    global app_name
    app_name = tk.StringVar(kill)
    tk.Entry(kill, textvariable = app_name, width = 35, borderwidth = 5).place(x= 8, y= 20)
    tk.Button(kill, text = "Kill", width = 14, height = 2, fg = 'white', bg = 'dodgerblue', borderwidth=0,
            highlightthickness=0, command = lambda: send_kill(client_socket), relief="flat").place(x= 300, y= 13)
    return
        
class App_Control_UI(Frame):
     def __init__(self, parent, client_socket):    
        Frame.__init__(self, parent)
        self.configure(
            #window,
            bg = "black",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        parent.geometry("1280x720+200+200")
        self.grid(row=0, column=0, sticky="nsew")

        #backround
        self.back_gound_image = ImageTk.PhotoImage(Image.open(path("bg3.jpg")))
        self.back_gound_label = Label(self, image=self.back_gound_image, bg='black')
        self.back_gound_label.pack(fill=X)

        self.tab = ttk.Treeview(self, height = 18, selectmode='browse')
        self.scroll = tk.Scrollbar(self, orient = "vertical", command = self.tab.yview)
        self.scroll.place(
            x=850,
            y=120,
            height=404
        )
        self.tab.configure(yscrollcommand = self.scroll.set)
        self.tab['columns'] = ("Name", "ID", "Count")
        self.tab.column('#0', width=0)
        self.tab.column("Name", anchor="center", width = 150, minwidth = 10, stretch = True)
        self.tab.column("ID", anchor="center", width = 150, minwidth = 10, stretch = True)
        self.tab.column("Count", anchor="center", width = 150, minwidth = 10, stretch = True)
        self.tab.heading('#0', text='')
        self.tab.heading("Name", text = "Name Application")
        self.tab.heading("ID", text = "ID Application")
        self.tab.heading("Count", text = "Count Threads")
        self.tab.place(
            x=140,
            y=120,
            width=713,
            height=404
        )

        self.button_list = Button(self, text = 'LIST', width = 20, height = 5, fg = 'white', bg = 'dodgerblue',
            borderwidth=0,
            highlightthickness=0,
            command=lambda: list_app(client_socket, self.tab),font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_list.place(
            x=910,
            y=139,
            width=135,
            height=50
        )

        self.button_start = Button(self, text = 'START', width = 20, height = 5, fg = 'white', bg = 'dodgerblue',
            borderwidth=0,
            highlightthickness=0,
            command=lambda: start(parent, client_socket),font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_start.place(
            x=910,
            y=219,
            width=135,
            height=50
        )

        self.button_kill = Button(self, text = 'KILL', width = 20, height = 5, fg = 'white', bg = 'dodgerblue',
            borderwidth=0,
            highlightthickness=0,
            command=lambda: kill(parent, client_socket),font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_kill.place(
            x=910,
            y=299,
            width=135,
            height=50
        )

        self.button_clear = Button(self, text = 'CLEAR', width = 20, height = 5, fg = 'white', bg = 'dodgerblue',
            borderwidth=0,
            highlightthickness=0,
            command=lambda: clear(self.tab),font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_clear.place(
            x=910,
            y=379,
            width=135,
            height=50
        )
        
        self.button_back = Button(self, text = 'BACK', width = 20, height = 5, fg = 'white', bg = 'dodgerblue',
            borderwidth=0,
            highlightthickness=0,font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_back.place(
            x=910,
            y=459,
            width=135,
            height=50
        )
