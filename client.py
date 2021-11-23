import socket
import threading

PORT = 5050
HOST = '127.0.0.1'
FORMAT = 'utf-8'
ADDR = (HOST, PORT)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting  server")
s.connect(ADDR)

print("please Enter your username and password (format 'Username' space 'password') to login/signup")

def get_message():
    while True:
        response = s.recv(1024).decode(FORMAT)
        print(response)
        if response == 'bye':
            break


read_Thread = threading.Thread(target=get_message)
read_Thread.start()

while True:
    message = input()
    s.sendall(message.encode(FORMAT))
    