import  pickle, psutil, struct
import os
import subprocess
BUFSIZ = 1024 * 4

def send_data(client_socket, data):
    size = struct.pack('!I', len(data))
    data = size + data
    client_socket.sendall(data)
    return

def list_processes():
    list1 = list()
    list2 = list()
    list3 = list()
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            name = proc.name()
            pid = proc.pid
            threads = proc.num_threads()
            list1.append(str(name))
            list2.append(str(pid))
            list3.append(str(threads))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return list1, list2, list3

def kill(process_id):
    cmd = 'taskkill.exe /F /PID ' + str(process_id)
    try:
        a = os.system(cmd)
        if a == 0:
            return 1
        else:
            return 0
    except:
        return 0

def start(name):
    subprocess.Popen(name)
    return


def process_control(client_socket):
    global msg
    while True:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if "QUIT" in msg and len(msg) < 20:
            return
        result = 0
        list1 = list()
        list2 = list()
        list3 = list()
        option = int(msg)
        #0 - đóng 1 process
        if option == 0:
            process_id = client_socket.recv(BUFSIZ).decode("utf8")
            process_id.lower()
            kill(process_id)
            result = 1
        #1 - xem danh sách process
        elif option == 1:
            try:
                list1, list2, list3 = list_processes()
                result = 1
            except:
                result = 0
        #2 - xóa bảng
        elif option == 2:
            result = 1
        #3 - mở 1 process
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
            list1 = pickle.dumps(list1)
            list2 = pickle.dumps(list2)
            list3 = pickle.dumps(list3)

            send_data(client_socket, list1)   
            send_data(client_socket, list2)
            send_data(client_socket, list3)
    return
