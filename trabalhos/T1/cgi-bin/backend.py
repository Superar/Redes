import sys
import socket
import re

from protocolo import *


exclude_list = ['|', '>', ';']

maq_ports = {'maq1': 9000,
           'maq2': 9000,
           'maq3': 9000}

HOST = '127.0.0.1'
PORT = 9001

# Comandos recebidos do webserver
commands = sys.stdin.readlines()
commands_str = ''.join(commands)

# Verifica se algum comando possui algum dos itens em exclude_list
# Retorna erro caso sim
if [x for x in exclude_list if x in commands_str]:
    print 'Argumentos invalidos: ' + str(exclude_list)
    raise ValueError

# Conexao e execucao dos comandos para cada maquina
for maq in sorted(maq_ports.keys()):

    # Encontra todos os comandos a serem executados para a maquina atual
    regex = '(?:' + maq + r')\S+(?=\n)'
    exec_list = re.findall(regex, commands_str)
    exec_list = [c.split('#') for c in exec_list]
    
    if exec_list:
        print '<h1>' + maq + '</h1>'
        try:
            # Conexao
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect(('localhost', maq_ports[maq]))
        except Exception as ex:
            # Conexao malsucedida
            print 'backend.py'
            print ex
        else:
            # Conexao bem-sucedida
            # Envia cada comando separadamente
            for cmd in exec_list:
                # Criacao do pacote       
                print '<h2>' + cmd[1] + '</h2>'
                msg = Message()
                msg.request('127.0.0.2', cmd[1:], 1)
                data = msg.encode()
                data.seek(0)

                # Envio dos dados
                sock.sendall(data.read())
                
                # Recebimento de resposta e decodificacao
                data_response = sock.recv(1024)
                buffer = io.BytesIO(data_response)
                response = Message()
                response.decode(buffer)

                print '<pre>' + response.content + '</pre>'
        finally:
            # Ao final, socket e fechado para se conectar a proxima maquina
            sock.shutdown(socket.SHUT_WR)
            sock.close()
