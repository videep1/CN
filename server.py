import socket
from datetime import date
import threading



PORT = 5050
HOST = '127.0.0.1'
FORMAT = 'utf-8'

ADDR = (HOST, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []


clients_user = []
clients_password = []
admin_username = "admin"
admin_password = "admin"
admin_logged_in = False
admin_object = None
def broadcast(client, message, addr, user=""):
    msg = f"<{user}>: {message}"
    for client in clients:
        try:
            client.sendall(msg.encode(FORMAT))
        except:
            client.close()
            remove(client)

def remove(client):
    if client in clients:
        clients.remove(client)


def handle(client, addr):
    global admin_logged_in, admin_password, admin_username, admin_object
    
    user_logged_in = False
    user = ""
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
        except:
            client.close()
            print("Connection with ", addr, "closed")
            print("connected clients: ", threading.active_count() - 1)
            remove(client)
            break
        if not user_logged_in:
            msgs = msg.split(" ")
            idx = -1
            try:
                idx = clients_user.index(msgs[0])
            except:
                pass
            if idx == -1:
                clients_user.append(msgs[0])
                user = msgs[0]
                clients_password.append(msgs[1])
                if user=="admin":
                    client.sendall("admin Logged in.\n".encode(FORMAT))
                else:
                    client.sendall("new user registered. Logged in.\n".encode(FORMAT))
                if user == admin_username:
                    for c in clients_user:
                        s="\n" + c + " joined the meet\n"
                        client.sendall(s.encode(FORMAT))
                    admin_logged_in = True
                    admin_object = client
                else:
                    if admin_logged_in:
                        admin_object.sendall(("\n" + user + " joined the meet\n").encode(FORMAT))
                user_logged_in = True
            else:
                if clients_password[idx] == msgs[1]:
                    user_logged_in = True
                    user = msgs[0]
                    client.sendall("Logged in\n".encode(FORMAT))
                    if user == admin_username:
                        admin_logged_in = True
                else:
                    client.sendall("Login failed. flase credentials.\n".encode(FORMAT))
                    remove(client)
            continue
        if admin_logged_in:
            broadcast(client, msg, addr, user)
        else:
            client.sendall("Admin didn't start  meet yet.\n".encode(FORMAT))






def start():
    server.listen(100)
    print("Server started")
    while True:
        client, addr = server.accept()
        print("Connected with ", addr, " ")
        clients.append(client)
        print("Connection from", addr)
        thread = threading.Thread(target=handle, args=(client, addr))
        thread.start()
        print("connected clients: ", threading.active_count() - 1)

start()