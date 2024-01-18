import cv2
import numpy as np
import struct
import zlib
import keyboard
from tkinter import*


def read_event(default_value):
    if keyboard.is_pressed('esc'):
         return keyboard.read_event().name
    else:
         return default_value


def livescreen(client_socket):
    while True:
        key = read_event(' ')
        if key == 'esc': 
            client_socket.send('E'.encode())
            cv2.destroyWindow("Screen")
            break
        else: client_socket.send(key.encode())
        # Nhận kích thước dữ liệu ảnh
        size_data = b""
        while len(size_data) < 4:
            size_data += client_socket.recv(4 - len(size_data))
        size = struct.unpack(">L", size_data)[0]

        # Nhận dữ liệu ảnh
        img_data = b""
        while len(img_data) < size:
            img_data += client_socket.recv(size - len(img_data))

        # Giải nén và hiển thị ảnh
        img_data = zlib.decompress(img_data)
        img = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Screen", img)
        cv2.waitKey(1)

#import os
#import socket
#from PIL import ImageGrab
#import keyboard
#import struct
#import cv2
#import numpy as np
#import socket
#import zlib
#import pyautogui

#def liveScreen(client_socket):
#    while True:
#        key = client_socket.recv(1).decode()
#        if key == 'E': 
#            #cv2.destroyWindow("Screen")
#            break
#        # Chụp màn hình
#        img = pyautogui.screenshot()
#        img = np.array(img)

#        # Nén ảnh
#        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#        img = cv2.resize(img, (0, 0), fx=1, fy=1)
#        _, img_encoded = cv2.imencode(".png", img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
#        img_data = zlib.compress(img_encoded, 9)

#        # Gửi kích thước dữ liệu ảnh trước
#        size = struct.pack(">L", len(img_data))
#        client_socket.sendall(size)

#        # Gửi dữ liệu ảnh
#        client_socket.sendall(img_data)
