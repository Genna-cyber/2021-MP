#!/usr/bin/env python
# coding: utf-8

# In[5]:


import threading
import random
import time
import socket

class FileExecutor():
    
    def writeName(self, name):   
        f = open('name.txt', 'a')
        f.write(name + '\n')
        f.close()
    
    def writeLog(self, data):
        f = open('data.txt', 'a')
        f.write(time.ctime() + data + '\n')
        f.close()

class Filter():   
    
    def addWord(self, data):
        for line in self.showList():
            if data.lower() == line:
                return          
        f = open('badWords.txt', 'a')
        f.write(data.lower() + '\n')
        f.close()          
    
    def showList(self):
        f = open('badwords.txt', 'r')
        lines = f.read().splitlines()
        return lines 
    
    def censor(self, data, name):
        for line in self.showList():
            if data.lower().endswith(line.lower()):
                print("Ya vse mame rakawu!")
                data = '***'
                break
        data = '['+name+']' + '->'+ data
        return data

class Client():
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port
        
    def receive(self, client, server):
        while True:
            try:
                data,addr = client.recvfrom(1024)
                print(data.decode('utf-8'))
            except:
                print("Error!")
                client.close()
                break           
    
    def write(self, client, server):
        filter_class = Filter()
        fileExecutor = FileExecutor()
        name = input('Your nickname: ')
        if name == '':
            name = 'Guest'+str(random.randint(1000,9999))
        print('Your name is:'+name)
        fileExecutor.writeName(name)
        client.sendto(name.encode('utf-8'),server)
        while True:
            data = input()
            if data == 'qqq':
                break
                
            elif data=='':
                continue
                
            elif data == '/addWord':
                print("Izu4eno novoe slovo:")
                ban = input()
                filter_class.addWord(ban)
                continue
                
            elif data == '/showBadWords':
                print ("Slovarek Translitnogo mata: ", filter_class.showList())
                continue     
            data = filter_class.censor(data, name) 
            fileExecutor.writeLog(data)
            client.sendto(data.encode('utf-8'),server)
        message = name + " live the chat!"
        client.sendto(message.encode('utf-8'),server)    
        client.close()
        
    def runClient(self):
        pass
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client.bind((self.getHost(),self.getPort())) 
        print('Client IP->'+str(self.getHost())+' Port->'+str(self.getPort()))
        server = (str(self.getHost()),5000)
        
        receive_thread = threading.Thread(target=self.receive, args=(client, server))
        receive_thread.start()
        write_thread = threading.Thread(target=self.write, args=(client, server))
        write_thread.start()
        
        
        
myHostName = socket.gethostname()
host = socket.gethostbyname(myHostName)
port = random.randint(6000,10000)   
client = Client(host, port)
client.runClient()


# In[ ]:




