import tkinter as tk
import socket
from tkinter import messagebox
import app_control_client
import keyboard_client
import screenshot_client
import shutdown_client
import mouse_client
import process_control_client
import livescreen_client
import file_control_client
import multi_task
from Homescreen_GUI import Homescreen_UI
import socket
from tkinter import*
from tkinter.ttk import*

#global variables
BUFSIZ = 1024 * 4
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global client_socket
global host_id
app = Tk()
app.geometry("1200x600")
app.configure(bg = "#FFFFFF")
app.title('Client')
app.resizable(False, False)

def get_input_value():
    value = entry.get()
    main.destroy()  # Đóng cửa sổ sau khi nhập giá trị
    return value  # In giá trị của biến

main = tk.Tk()
main.geometry("300x150")
main.title("Client")
main['bg'] = '#000000'
# Tạo label
label = tk.Label(main, text="Nhập địa chỉ IP của server:")
label.pack(pady=10)

# Tạo entry để nhập giá trị
entry = tk.Entry(main)
entry.pack()

def back(temp,client_socket):
    temp.destroy()
    frame_hp.tkraise()
    client_socket.sendall(bytes("QUIT", "utf8"))

def back_key(temp,client_socket):
    temp.destroy()
    frame_hp.tkraise()

def app_control(client_socket):
    client_socket.sendall(bytes("APP_CONTROL", "utf8"))
    temp = app_control_client.App_Control_UI (app, client_socket)
    temp.button_back.configure(command = lambda: back(temp,client_socket))
    return

def process_control(client_socket):
    client_socket.sendall(bytes("PROCESS_CONTROL", "utf8"))
    temp = process_control_client.Process_Control_UI(app, client_socket)
    temp.button_back.configure(command = lambda: back(temp, client_socket))
    return

def screenshot(client_socket):
    client_socket.sendall(bytes("SCREENSHOT", "utf8"))
    temp = screenshot_client.recv_screenshot(client_socket) 
    #back(temp)
    return

def file_control(client_socket):
    client_socket.sendall(bytes("FILE CONTROL", "utf8"))
    temp = file_control_client.File_Control_UI(app, client_socket)
    temp.button_back.configure(command = lambda: back(temp,client_socket))
    return


def livescreen(client_socket):
    client_socket.sendall(bytes("LIVESCREEN", "utf8"))
    temp = livescreen_client.livescreen(client_socket) 
    #back(temp)
    return
    
def disconnect(client_socket):
    client_socket.sendall(bytes("QUIT", "utf8"))
    frame_hp.destroy()
    app.destroy()
    return

def keyboard(client_socket):
    client_socket.sendall(bytes("KEYBOARD", "utf8"))
    temp = keyboard_client.Keyboard_UI(app, client_socket)
    temp.button_back.configure(command = lambda: back_key(temp,client_socket))
    return

def shutdown(client_socket): 
    client_socket.sendall(bytes("SHUTDOWN", "utf8"))
    temp = shutdown_client.shutdown_UI(client_socket, app)
    temp.button_no.configure(command = lambda: back(temp,client_socket))
    return
  
def back_reg(temp):
    temp.client_socket.sendall(bytes("STOP_EDIT_REGISTRY", "utf8"))
    temp.destroy()
    frame_hp.tkraise()

def mouse_control(client_socket):
    client_socket.sendall(bytes("MOUSE", "utf8"))
    temp = mouse_client.server_mouse_control(client_socket) #Sẽ viết hàm UI cho mouse control sau


def Multi_task(client_socket, IP):
    client_socket.sendall("MULTI TASK".encode())
    screen_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_con.connect((IP,8888))
    key_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    key_con.connect((IP,8888))
    mouse_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_con.connect((IP,8888))
    temp = multi_task.Control(app, client_socket, screen_con, key_con, mouse_con)
    #temp.button_back.configure(command = lambda: back(temp,client_socket))
    return
    


def show_main_ui(client_socket):
    #frame_lg.destroy()
    global frame_hp
    frame_hp = Homescreen_UI(app)
    frame_hp.button_app_control.configure(command = lambda: app_control(client_socket))
    frame_hp.button_process_control.configure(command = lambda: process_control(client_socket))
    frame_hp.button_shut_down.configure(command = lambda: shutdown(client_socket))
    frame_hp.button_screenshot.configure(command = lambda: screenshot(client_socket))
    frame_hp.button_livescreen.configure(command = lambda: livescreen(client_socket))
    frame_hp.button_disconnect.configure(command = lambda: disconnect(client_socket))
    frame_hp.button_keyboard.configure(command = lambda: keyboard(client_socket))
    frame_hp.button_mouse_control.configure(command = lambda: mouse_control(client_socket))
    frame_hp.button_file_control.configure(command = lambda: file_control(client_socket))
    frame_hp.button_multi_task.configure(command = lambda: Multi_task(client_socket, host_id)) 
    return

def Connect():
    global host_id
    host_id=get_input_value()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host_id, 8888)
    client_socket.connect(server_address)
    messagebox.showinfo(message = "Kết nối thành công!")
    while True:
        show_main_ui(client_socket)
        app.mainloop()
    client_socket.close()
###############################################################################    

tk.Button(main, text = "CONNECT", width = 10, height = 2, fg = 'white', bg = 'dodgerblue', borderwidth=0,
            highlightthickness=0, command = Connect, relief="flat").place(x = 150, y = 100, anchor = "center")
main.mainloop()
