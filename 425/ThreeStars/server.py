#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import threading
import queue

class Server():
    def __init__(self, host, port,  recvPackets = queue.Queue()):
        self.host = host
        self.port = port
        self.recvPackets = recvPackets
    
    def getHost(self):
        return self.host
        
    def getPort(self):
        return self.port 

    def getQueue(self):
        return self.recvPackets
     
    def broadcast(self, server, message, clients): 
        for client in clients:
            server.sendto(message.encode('utf-8'), client)
        
    def receive(self, sock, recvPackets):
        while True:
            data,addr = sock.recvfrom(1024)
            recvPackets.put((data,addr))

    def runServer(self):
        pass
        print('Server hosting on IP-> '+str(self.getHost()))
        server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server.bind((self.getHost(),self.getPort()))
        print('Server Running...')
    
        receive_thread = threading.Thread(target=self.receive, args=(server, self.getQueue(),))
        receive_thread.start()
        handle_thread = threading.Thread(target=self.handle, args=(server, self.getQueue(),))
        handle_thread.start()
        
    def greetings(self,i):
        f = open('name.txt', 'r')
        lines = f.read().splitlines()
        name = lines[i]
        message = name + " joined the chat! You can use commands: /addWord  and  /showBadWords"
        return message
        
    
    def handle(self, server, recvPackets):
        clients = set()
        i = 0
        while True:
            while not recvPackets.empty():
                data,addr = recvPackets.get()
                if addr not in clients:
                    clients.add(addr)
                    self.broadcast(server, self.greetings(i), clients)
                    i += 1
                    continue
                data = data.decode('utf-8')
                if data.endswith('qqq'):
                    clients.remove(addr)
                    continue
                print(str(addr)+data)
                for c in clients:
                    if c!=addr:
                        server.sendto(data.encode('utf-8'),c)
        server.close()

host = socket.gethostbyname(socket.gethostname())
port = 5000
server = Server(host, port,)
server.runServer()
open('name.txt', 'w').close()
open('data.txt', 'w').close()

