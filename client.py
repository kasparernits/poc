import socket

s = socket.socket()

port = 8080

try:
    s.connect(('127.0.0.1', port))
except socket.error:
    print("Failed to connect")

print(s.recv(1024).decode())

s.close()

