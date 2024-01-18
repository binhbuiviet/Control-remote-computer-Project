import os
import tkinter as tk
import tkinter.ttk as ttk
import pickle
from tkinter import Text, Button,filedialog, messagebox, Frame
from tkinter import*
from PIL import Image, ImageTk


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 

import os
import sys
def path(file_name):
    file_name = 'pic\\' + file_name
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)

def listDirs(client_socket, path):
    client_socket.sendall(path.encode())

    data_size = int(client_socket.recv(BUFFER_SIZE))
    if (data_size == -1):
        messagebox.showerror(message = "Nhấn vào nút SHOW một lần nữa để xem danh sách thư mục!")
        return []
    client_socket.sendall("received filesize".encode())
    data = b""
    while len(data) < data_size:
        packet = client_socket.recv(999999)
        data += packet
    if (data == "error"):
        messagebox.showerror(message = "Không thể mở được thư mục!")
        return []
    
    list_folder_file = pickle.loads(data)
    return list_folder_file

class File_Control_UI(Frame):
    def __init__(self, parent, client_socket):
        Frame.__init__(self, parent)

        self.configure(bg = "black",height = 720,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
        parent.geometry("1280x720+200+200")
        self.grid(row=0, column=0, sticky="nsew")


        ##backround
        self.back_gound_image = ImageTk.PhotoImage(Image.open(path("bg3.jpg")))
        self.back_gound_label = Label(self, image=self.back_gound_image, bg='black')
        self.back_gound_label.pack(fill=X)
        
        self.client = client_socket
        self.currPath = " "
        self.nodes = dict()

        self.frame = tk.Frame(self, height = 360, width = 600)
        self.frame.place(x=250,y=120,width=600,height=360)

        self.tree = ttk.Treeview(self.frame)
        self.scroll_y = tk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scroll_x = tk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=self.scroll_y.set, xscroll=self.scroll_x.set)
        self.tree.pack(fill = tk.BOTH, expand = True)

        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind("<<TreeviewSelect>>", self.select_node)

        self.path = Text(self.frame, height = 1, width = 26, state = "disable")
        self.path.pack(side = tk.BOTTOM, fill = tk.X)

        self.button_show = Button(self, text = 'SHOW LIST', width = 20, height = 5,
            command=self.showTree,
            fg = 'white', bg = 'dodgerblue', font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_show.place(x=880,y=120,width=150,height=53)
        
        self.button_send = Button(self, text = 'SEND FILE', width = 20, height = 5,
            command=self.sendFileToServer,
            fg = 'white', bg = 'dodgerblue', font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_send.place(x=880,y=190,width=150,height=53)
        
        self.button_get = Button(self, text = 'GET FILE', width = 20, height = 5, 
            command=self.getFileFromServer,
            fg = 'white', bg = 'dodgerblue', font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_get.place(x=880,y=260,width=150,height=53)

        self.button_delete = Button(self, text = 'DELETE FILE', width = 20, height = 5, 
            command=self.deleteFile,
            fg = 'white', bg = 'dodgerblue', font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_delete.place(x=880,y=330,width=150,height=53)

        self.button_back = Button(self, text = 'BACK', width = 20, height = 5,
            command=lambda: self.back(),
            fg = 'white', bg = 'dodgerblue', font='Helvetica 12 bold',
            relief="flat"
        )
        self.button_back.place(x=880,y=400,width=150,height=53)

    def insert_node(self, parent, text, abspath, isFolder):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if abspath != "" and isFolder:
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            try:
                dirs = listDirs(self.client, abspath)
                for p in dirs:
                    self.insert_node(node, p[0], os.path.join(abspath, p[0]), p[1])
            except:
                messagebox.showerror(message = "Không thể mở được thư mục này!")

    def select_node(self, event):
        item = self.tree.selection()[0]
        parent = self.tree.parent(item)
        self.currPath = self.tree.item(item,"text")
        while parent:
            self.currPath = os.path.join(self.tree.item(parent)['text'], self.currPath)
            item = parent
            parent = self.tree.parent(item)

        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.insert(tk.END, self.currPath)
        self.path.config(state = "disable")

    def deleteTree(self):
        self.currPath = " "
        self.path.config(state = "normal")
        self.path.delete("1.0", tk.END)
        self.path.config(state = "disable")
        for i in self.tree.get_children():
            self.tree.delete(i)

    def showTree(self):
        self.deleteTree()
        self.client.sendall("SHOW".encode())

        data_size = int(self.client.recv(BUFFER_SIZE))
        data = b""
        while len(data) < data_size:
            packet = self.client.recv(999999)
            data += packet
        loaded_list = pickle.loads(data)
        
        for path in loaded_list:
            try:
                abspath = os.path.abspath(path)
                self.insert_node('', abspath, abspath, True)
            except:
                continue

    # copy file from client to server
    def sendFileToServer(self):
        if not os.path.isdir(self.currPath):
            messagebox.showinfo(message = "Bạn hãy chọn thư mục bên server để nhận file!")
            return []
        self.client.sendall("SEND".encode())
        filename = filedialog.askopenfilename(title="Select File", 
                                                filetypes=[("All Files", "*.*")])
        if filename == None or filename == "":
            self.client.sendall("-1".encode())
            temp = self.client.recv(BUFFER_SIZE)
            return 
        destPath = self.currPath + "\\"
        filesize = os.path.getsize(filename)
        self.client.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{destPath}".encode())
        isReceived = self.client.recv(BUFFER_SIZE).decode()
        if (isReceived == "server was received filename"):
            try:
                with open(filename, "rb") as fin:
                    data = fin.read()
                    self.client.sendall(data)
            except:
                self.client.sendall("-1".encode())
            isReceivedContent = self.client.recv(BUFFER_SIZE).decode()
            if (isReceivedContent == "server was received content of file"):
                messagebox.showinfo(message = "Gửi tệp tin thành công!")
                return True

    # copy file from server to client
    def getFileFromServer(self):
        if os.path.isdir(self.currPath):
            messagebox.showinfo(message = "Bạn hãy chọn file muốn lấy của server!")
            return []
        self.client.sendall("GET".encode())
        try:
            destPath = filedialog.askdirectory()
            if destPath == None or destPath == "":
                self.client.sendall("-1".encode())
                temp = self.client.recv(BUFFER_SIZE)
                return 
            self.client.sendall(self.currPath.encode())
            filename = os.path.basename(self.currPath)
            filesize = int(self.client.recv(100))
            if (filesize == -1):
                messagebox.showerror(message = "Không thể lấy tệp tin!")  
                return
            self.client.sendall("received filesize".encode())
            data = b""
            while len(data) < filesize:
                packet = self.client.recv(999999)
                data += packet
            with open(destPath + "\\" + filename, "wb") as f:
                f.write(data)
            messagebox.showinfo(message = "Lấy tệp tin thành công!")
        except:
            messagebox.showerror(message = "Không thể lấy tệp tin!")  


    def deleteFile(self):
        if os.path.isdir(self.currPath):
            messagebox.showinfo(message = "Bạn hãy chọn file muốn xóa của server!")
            return []
        self.client.sendall("DELETE".encode())
        self.client.sendall(self.currPath.encode())
        res = self.client.recv(BUFFER_SIZE).decode()
        if (res == "deleted"):
            messagebox.showinfo(message = "Xóa tệp tin thành công!")
        else:
            messagebox.showerror(message = "Không thể xóa được tệp tin!") 

    def back(self):
        return
