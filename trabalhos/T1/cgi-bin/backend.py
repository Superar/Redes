import sys
import socket
import re


maq_ips = {'maq1': '0.0.0.0',
           'maq2': '0.0.0.1',
           'maq3': '0.0.0.2'}

HOST = '0.0.0.0'
PORT = '9999'


commands = sys.stdin.readlines()
commands_str = ''.join(commands)

for maq in maq_ips:
    regex = '(?:' + maq + r')\S+(?=\n)'
    exec_list = re.findall(regex, commands_str)
    exec_list = [c.split('#') for c in exec_list]
    print(exec_list)
 
