# -*- coding: utf-8 -*-
import socket
import sys
import threading

class Server():
    def __init__(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            #serversocket.bind((socket.gethostname(), 80))
            serversocket.bind(("0.0.0.0", 90))
        except socket.error as msg:
            print("Bind failed. Error Code : %s Message %s " %(str(msg[0]), str(msg[1])))
            sys.exit()
        try:
            serversocket.listen(5)
            while True:
                # Wait to accept a connection - blocking call
                conn, addr = serversocket.accept()
                print("Connection with %s : %s " %(addr[0], str(addr[1])))
                hilo = threading.Thread(target=self.clientthread, args=(conn,))
                hilo.start()
        finally:
            serversocket.close()

    def clientthread(self,conn):
        conn.send("Welcome to the server. Type something! \n".encode()) # send only takes string
        while True:
            data = conn.recv(1024)
            reply = "OK..." + str(data)
            if not data:
                break
            conn.sendall(reply.encode())
        conn.close()

class Client():
    def __init__(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("0.0.0.0", 8000))
        client.send("Hello".encode())
        print(client.recv(1024))
        try:
            while True:
                message = input(">> ")
                client.send(message.encode())
                print("<< "+str(client.recv(1024)))
                if message == "close":
                    break
        finally:
            client.close()

if __name__ == "__main__":
    server = Server()
    #client= Client()
