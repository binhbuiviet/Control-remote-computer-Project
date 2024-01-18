from time import sleep
import keyboard
import pyautogui
import struct

def read_event_or_default(default_value):
    if keyboard.is_pressed('x') or keyboard.is_pressed('z') or keyboard.is_pressed('esc'):
         return keyboard.read_event().name
    else:
         return default_value


def server_mouse_control(client_socket):
    while True:
         # Sử dụng hàm read_event_or_default để đọc sự kiện từ bàn phím hoặc trả về giá trị mặc định
        key = read_event_or_default(' ')
        if key == 'esc': 
            client_socket.send('E'.encode())
            break
        else: client_socket.send(key.encode())
        data="";
        pos = pyautogui.position()
        # Mã hóa số nguyên thành dạng bytes để gửi qua socket
        data = struct.pack('!ii', pos[0], pos[1])
        client_socket.sendall(data)  # Gửi toàn bộ dữ liệu trong một lần gửi
        sleep(0.1)



