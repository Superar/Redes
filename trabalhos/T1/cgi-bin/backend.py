import sys
import socket
import re

from protocolo import *

# Caracteres que indicam parametros maliciosos
exclude_list = ['|', '>', ';']

# Mapeamento das maquinas e seus respectivos enderecos 
# (no nosso caso, as portas onde cada daemons esta escutando)
maq_addrs = {'maq1': ['127.0.0.1', 9001],
             'maq2': ['127.0.0.1', 9002],
             'maq3': ['127.0.0.1',9003]}

# Porta utilizada pelo backend para a comunicacao atraves do socket
PORT = 9000

# Comandos recebidos do webserver
commands = sys.stdin.readlines()
commands_str = ''.join(commands)

# Verifica se algum comando possui algum dos itens em exclude_list
# Retorna erro caso sim
if [x for x in exclude_list if x in commands_str]:
    print 'Argumentos invalidos: ' + str(exclude_list)
    raise ValueError

# Conexao e execucao dos comandos para cada maquina
for maq in sorted(maq_addrs.keys()):

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
            # Se conecta com a maquina especificada
            sock.connect((maq_addrs[maq][0], maq_addrs[maq][1]))
        except Exception as ex:
            # Conexao malsucedida
            print 'backend.py'
            print ex
        else:
            # Conexao bem-sucedida
            # Envia cada comando separadamente
            for cmd in exec_list:
                print '<h2>' + cmd[1] + '</h2>'
                # Criacao do pacote de requisicao       
                msg = Message()
                msg.request(maq_addrs[maq][0], cmd[1:], 1)
                
                response = msg.send(sock)

                print '<pre>' + response.content + '</pre>'
        finally:
            # Ao final, socket e fechado para se conectar a proxima maquina
            sock.shutdown(socket.SHUT_WR)
            sock.close()
