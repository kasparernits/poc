import socket
import paramiko
import sys

s = socket.socket()

port = 3022

try:
    s.connect(('127.0.0.1', port))
except socket.error:
    print("Failed to connect")

transport = paramiko.transport.Transport(s)
try:
    transport.start_client()
except paramiko.ssh_exception.SSHException:
    print('[-] Failed to negotiate SSH transport')
    sys.exit(2)


try:
    transport.auth_publickey('zero00', paramiko.RSAKey.generate(2048))
except paramiko.ssh_exception.AuthenticationException:
    print('[+] Valid username')


print(s.recv(1024).decode())

s.close()

