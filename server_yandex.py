import socket
import threading
from time import sleep

ya_sock = socket.socket()
address = ("5.255.255.242", 443)
ya_sock.connect(address)

data_out = b"GET / HTTP/1.1\r\nHost:ya.ru\r\n\r\n"
ya_sock.send(data_out)
data_in = b""

def receiving():
    global data_in
    while True:
        data_chunk = ya_sock.recv(1024)
        data_in = data_in + data_chunk

rec_thread = threading.Thread(target=receiving)
rec_thread.start()

sleep(4)
ya_sock.close()
print(data_in)