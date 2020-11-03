import argparse
import pickle
import socket
import json
import os
import sys
import optparse
from itertools import cycle

class Server:

    def _init_(self, interface, port):
        self.interface = interface
        self.port = port

    def change_text(self, text, d_string):
        w = text.split()
        fin_dict = eval(d_string)
        
        for i in w:
            if i in fin_dict.keys():
                text = text.replace(i, fin_dict[i])
        return text

    def enc_dec(self, text, key):
        encoded_text = ""
        
        for i in range(len(text)):
            c = text[i]
            k= key[i%len(key)]
            encoded_text +=chr(ord(c) ^ ord(k))
        return encoded_text

    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface, self.port))
        sock.listen(1)
        print('Listening at', sock.getsockname())

        while True:
            sc, sockname = sock.accept()
            print('We have accepted the connection from:', sockname)
            print('Socket name:', sc.getsockname())
            print('Socket peer:', sc.getpeername())
            mode, f1, f2 = sc.recv(self.MAX_BYTES).decode().split('ı')

            if mode == "change_text":
                chd = self.change_text(f1, f2)
                sc.sendall(chd.encode("ascii"))

            elif mode == "encode_decode":
                chd = self.enc_dec(f1, f2)
                sc.sendall(chd.encode())
            sc.close()
            print("Socket closed")

class Client:

    def _init_(self, port, host):
        self.port = port
        self.host = host
        
    def connect(self, mode, file, key):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        print("Socket:", sock.getsockname())
        first = os.path.getsize(file)
        second = os.path.getsize(key)
        sock.send(f"{mode}#{first}#{second}".encode())
        with open(file, "r") as f:
            firstd = f.read()
            print(firstd)
            print("Sending source file as bytes to server:")
            sock.sendall(bytes(firstd.encode()))
            print((firstd.encode()))
            f.close()
        with open(key, "r") as f:
            secondd = f.read() if mode == "encode_decode" else json.dumps(f)
            print(f'Sending {"json" if mode=="change_text" else "key"} file as  bytes to server:')
            sock.sendall(bytes(secondd.encode()))
            f.close()

        print("Received:")
        a = sock.recv(second).decode()
        print("Server:", str(a))
        sock.close()



    


    
            

            
