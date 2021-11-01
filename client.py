import socket
import threading

PORT = 5051
HOST = '127.0.0.1'
FORMAT = 'utf-8'
ADDR = (HOST, PORT)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to the server.....")
s.connect(ADDR)

def get_messages():
    while True:
        response = s.recv(2048).decode(FORMAT)
        print(response)


readThread = threading.Thread(target=get_messages)
readThread.start()

while True:
    message = input()
    s.sendall(message.encode(FORMAT))