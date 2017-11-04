import sys
import socket
import re

from protocolo import *


maq_ports = {'maq1': 9000,
           'maq2': 9000,
           'maq3': 9000}

HOST = '127.0.0.1'
PORT = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)            
sock.bind((HOST, PORT))

commands = sys.stdin.readlines()
commands_str = ''.join(commands)

for maq in maq_ports:
    regex = '(?:' + maq + r')\S+(?=\n)'
    exec_list = re.findall(regex, commands_str)
    exec_list = [c.split('#') for c in exec_list]
    
    sock.connect(('localhost', maq_ports[maq]))

    for cmd in exec_list:
        msg = Message()
        msg.request('127.0.0.2', cmd[1:], 1)
        data = msg.encode()
        data.seek(0)
        print msg.header
        sock.sendall(data.read())
