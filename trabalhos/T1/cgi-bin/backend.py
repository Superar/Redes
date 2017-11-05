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


for maq in sorted(maq_ports.keys()):
    regex = '(?:' + maq + r')\S+(?=\n)'
    exec_list = re.findall(regex, commands_str)
    exec_list = [c.split('#') for c in exec_list]
    
    if exec_list:
        print '<h1>' + maq + '</h1>'
        try: 
            sock.connect(('localhost', maq_ports[maq]))
        except Exception as ex:
            print 'backend.py'
            print ex

        for cmd in exec_list:       
            print '<h2>' + cmd[1] + '</h2>'
            msg = Message()
            msg.request('127.0.0.2', cmd[1:], 1)
            data = msg.encode()
            data.seek(0)

            sock.sendall(data.read())
            
            data_response = sock.recv(1024)
            buffer = io.BytesIO(data_response)
            response = Message()
            response.decode(buffer)

            print '<pre>' + response.content + '</pre>'
        
       # sock.shutdown(socket.SHUT_RDWR)
