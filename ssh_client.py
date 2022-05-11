import socket
import paramiko
import sys


class InvalidUsername(Exception):
    pass


s = socket.socket()

port = 3022

try:
    s.connect(('127.0.0.1', port))
except socket.error:
    print("Failed to connect")

t = paramiko.transport.Transport(s)
try:
    t.start_client()
except paramiko.ssh_exception.SSHException:
    print('[-] Failed to negotiate SSH transport')
    sys.exit(2)

try:
    t.auth_publickey('zero00', paramiko.RSAKey.generate(2048))
except InvalidUsername:
    print('[*] Invalid username')
    sys.exit(3)
except paramiko.ssh_exception.AuthenticationException:
    print('[+] Valid username')

# print(s.recv(1024).decode())

s.close()
