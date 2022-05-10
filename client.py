import socket

s = socket.socket()

port = 3022

try:
    s.connect(('127.0.0.1', port))
except socket.error:
    print("Failed to connect")

print(s.recv(1024).decode())

s.close()

