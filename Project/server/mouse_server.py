import pyautogui
import struct

def client_mouse_control(client_socket):
    while True:
        key = client_socket.recv(1).decode()
        if key == 'z': pyautogui.click(button='left')
        if key == 'x': pyautogui.click(button='right')
        if key == 'E': break
        x = client_socket.recv(4)
        y = client_socket.recv(4)
        # Giải mã số nguyên từ dữ liệu nhận được
        n1 = struct.unpack('!I', x)[0]
        n2 = struct.unpack('!I', y)[0]
        width, height = pyautogui.size()
        if n1 > width: pyautogui.moveTo(width, n2)
        elif n2 > height: pyautogui.moveTo(n1, height)
        else: pyautogui.moveTo(n1, n2)