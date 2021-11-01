import socket
import threading
import sys
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


#Allots the first argument of the string as the IP Address
IP_address = '127.0.0.1'
#Allocates the second argument as the port number
Port = 5051

#These are the values that the client must be aware about
server.bind((IP_address, Port))
server.listen(100)

list_of_clients=[]

Q = [" What is the 2+3? \n a.1 b.0 c.4 d.5",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit b.Celsius c.Rankine d.Kelvin",
     " Which sea creature has three hearts? \n a.Dolphin b.Octopus c.Walrus d.Seal",
     " Who was the character famous in our childhood rhymes associated with a lamb? \n a.Mary b.Jack c.Johnny d.Mukesh",
     " How many bones does a kid have? \n a.300 b.208 c.201 d.196"
     
     ]

A = ['d', 'a', 'b', 'a', 'a']

Count=[]
client = ["address",-1]
bzr =[0, 0, 0] #Buzzer List

def clientthread(conn, addr):
    conn.send(b"Hello Genius!!!\n Welcome to this quiz! Answer any 5 questions correctly before your opponents do\n Press any key on the keyboard as a buzzer for the given question\n")
    #Intro MSG
    # bzr arr 
    # 0 -> Buzzer pressed or not
    # 1 -> 
    # 2 -> question number

    # client arr
    # 0 -> COnnection conn
    # 1 -> Client number
    while True:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if bzr[0]==0:
                    client[0] = conn
                    bzr[0] = 1
                    i = 0
                    while i < len(list_of_clients):
                            if list_of_clients[i] == client[0]:
                                break
                            i +=1
                    client[1] = i

                elif bzr[0] ==1 and conn==client[0]:
                        bol = message[0] == A[bzr[2]][0]
                        print(A[bzr[2]][0])
                        if bol:
                            broadcast("player" + str(client[1]+1) + " +1" + "\n\n")
                            Count[i] += 1
                            if Count[i]==5:
                                broadcast("player" + str(client[1]+1) + " WON" + "\n")
                                end_quiz()
                                sys.exit()

                        else:
                            broadcast("player" + str(client[1]+1) + " -1" + "\n\n")
                            Count[i] -= 1
                        bzr[0]=0
                        if len(Q) != 0:
                            Q.pop(bzr[2])
                            A.pop(bzr[2])
                        if len(Q)==0:
                            end_quiz()
                        quiz()

                else:
                        x = " player " + str(client[1]+1) + " pressed buzzer first\n\n"
                        conn.send(x.encode())
            else:
                    remove(conn)

def broadcast(message):
    for clients in list_of_clients:
        try:
            clients.send(message.encode())
        except:
            clients.close()
            remove(clients)

def end_quiz():
    broadcast("Game Over\n")
    bzr[1]=1
    i = Count.index(max(Count))
    broadcast("player " + str(i+1)+ " wins!! by scoring "+str(Count[i])+" points.")
    for x in range(len(list_of_clients)):
        p = "You scored " + str(Count[x]) + " points."
        list_of_clients[x].send(p.encode())
        
    server.close()


def quiz():
    bzr[2] = random.randint(0,10000)%len(Q)
    if len(Q) != 0:
        for connection in list_of_clients:
            connection.send(Q[bzr[2]].encode())

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    Count.append(0)
    print(addr[0] + " connected")
    t = threading.Thread(target=clientthread, args=(conn,addr))
    t.start()
    if(len(list_of_clients)==2):
        
        quiz()

conn.close()
server.close()