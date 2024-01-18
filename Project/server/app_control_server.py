import  pickle, psutil, struct
import os
from AppOpener import open, close
BUFSIZ = 1024 * 4

def send_data(client_socket, data):
    size = struct.pack('!I', len(data))
    data = size + data
    client_socket.sendall(data)
    return

def list_apps():
    list_name = list()
    list_id = list()
    list_thread = list()
    temp = list()

    cmd = 'powershell "gps | where {$_.mainWindowTitle} | select Description, ID, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}'
    app = os.popen(cmd).read().split('\n')
    for line in app:
        if not line.isspace():
            temp.append(line)
    temp = temp[3:]
    for line in temp:
        try:
            arr = line.split(" ")
            if len(arr) < 3:
                continue
            if arr[0] == '' or arr[0] == ' ':
                continue

            name = arr[0]
            threads = arr[-1]
            ID = 0
            # interation
            cur = len(arr) - 2
            for i in range (cur, -1, -1):
                if len(arr[i]) != 0:
                    ID = arr[i]
                    cur = i
                    break
            for i in range (1, cur, 1):
                if len(arr[i]) != 0:
                    name += ' ' + arr[i]
            list_name.append(name)
            list_id.append(ID)
            list_thread.append(threads)
        except:
            pass
    return list_name, list_id, list_thread

def kill(name):
    close(name, match_closest = True, output = False)
    return
    
def start(name):
    open(name, match_closest = True)
    return


def app_control(client_socket):
    global msg
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if "QUIT" in msg and len(msg) < 20:
            return
        result = 0
        list_name = list()
        list_id = list()
        list_thread = list()
        option = int(msg)
        #0 - đóng 1 app
        if option == 0:
            pid = client_socket.recv(BUFSIZ).decode("utf8")
            pid.lower()
            kill(pid)
            result = 1
        #1 - xem danh sách app
        elif option == 1:
            try:
                list_name, list_id, list_thread = list_apps()
                result = 1
            except:
                result = 0
        #2 - xoa danh sách
        elif option == 2:
            result = 1
        #3 - mở 1 app
        elif option == 3:
            program_name = client_socket.recv(BUFSIZ).decode("utf8")
            try:
                program_name.lower()
                start(program_name)
                result = 1
            except:
                result = 0
        if option != 1 and option != 3:
            client_socket.sendall(bytes(str(result), "utf8"))
        if option == 1:
            list_name = pickle.dumps(list_name)
            list_id = pickle.dumps(list_id)
            list_thread = pickle.dumps(list_thread)

            send_data(client_socket, list_name)   
            send_data(client_socket, list_id)
            send_data(client_socket, list_thread)
    return
