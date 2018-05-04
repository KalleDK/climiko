import socket
import threading
import time


HOST = '127.0.0.1'
PORT = 51234
IAC  = bytes([255]) # "Interpret As Command"
DONT = bytes([254])
DO   = bytes([253])
WONT = bytes([252])
WILL = bytes([251])
theNULL = bytes([0])

SE  = bytes([240])  # Subnegotiation End
NOP = bytes([241])  # No Operation


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()


class chatServer(threading.Thread):
    def __init__(self, sock: socket.socket, addr):
        threading.Thread.__init__(self)
        self.socket = sock
        self.address = addr

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print('%s:%s connected.' % self.address)
        while True:
            try:
                data = self.socket.recv(1024)
            except:
                break
            print(data)
            self.socket.send(IAC + NOP)
            if not data:
                break
        self.socket.close()
        print('%s:%s disconnected.' % self.address)
        lock.acquire()
        clients.remove(self)
        lock.release()


while True:
    # wait for socket to connect
    # send socket to chatserver and start monitoring
    chatServer(*s.accept()).start()
