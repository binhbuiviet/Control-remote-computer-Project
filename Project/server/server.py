import socket
import app_control_server
import keyboard_server
import mouse_server
import livescreen_server
import process_control_server
import screenshot_server
import shutdown_server
import file_control_server
import multi_task


#Global variables
global server_socket
global client_socket
BUFSIZ = 1024 * 4

def app_control(client_socket):
    app_control_server.app_control(client_socket)
    return

def keyboard(client_socket):
    keyboard_server.recv_keyboard(client_socket)
    return

def file_control(client_socket):
    file_control_server.file_control(client_socket)
    return

def mouse(client_socket):
    mouse_server.client_mouse_control(client_socket)
    return

def process_control(client_socket):
    process_control_server.process_control(client_socket)
    return

def screenshot(client_socket):
    screenshot_server.send_screenshot(client_socket)
    return

def shutdown(client_socket):
    shutdown_server.shutdown(client_socket)
    return

def Livescreen(client_socket):
    livescreen_server.liveScreen(client_socket)
    return

def Multi_task(client_socket):
    screen_con, screen_addr = server_socket.accept()
    key_con, key_addr = server_socket.accept()
    mouse_con, mouse_addr = server_socket.accept()
    multi_task.controlled(client_socket, screen_con, key_con, mouse_con)
    screen_con.close()
    key_con.close()
    mouse_con.close()
    return

def main():
    #frame_lg.button_1.configure(command= lambda:connect(frame_lg))
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.1.12', 8888)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("Server is listening on port 8888...")
    client_socket, client_address = server_socket.accept()
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if "KEYBOARD" in msg:
            keyboard(client_socket)
        elif "SHUTDOWN" in msg:
            shutdown(client_socket)
        elif "LIVESCREEN" in msg:
            Livescreen(client_socket)
        elif "SCREENSHOT" in msg:
            screenshot(client_socket)
        elif "MOUSE" in msg:
            mouse(client_socket)
        elif "APP_CONTROL" in msg:
            app_control(client_socket)
        elif "PROCESS_CONTROL" in msg:
            process_control(client_socket)
        elif "MULTI TASK" in msg:
            Multi_task(client_socket)
        elif "FILE CONTROL" in msg:
            file_control(client_socket)
        elif "QUIT" in msg:
            client_socket.close()
            return
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()

