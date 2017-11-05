import socket
import threading
import sys
import getopt
import subprocess
from protocolo import *

# Definicao do localhost
HOST = '127.0.0.1'
# Definicao da porta padrao
PORT = 9000

class Daemon(threading.Thread):

    # Cria a thread de conexao com ip, porta e o socket para resposta
    def __init__(self, ip, port, sock):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.dest_sock = sock

    # Execucao da thread
    def run(self):
        
        tam = 1024

        while True:
            try:
                # Recebe os dados atraves do socket
                data = self.dest_sock.recv(tam)
                f = io.BytesIO(data)
                print sys.getsizeof(data)                
                # Se houve dados
                if data:
                    request = Message()
                    request.decode(f)

                    print request.header
                    response = self.get_response(request)            
                   
                    response = request.encode()
                    response.seek(0)
                    print 'envia'
                    self.dest_sock.sendall("Olar tudo bem")
                else:
                    raise error('Desconectado')
            except:
                self.dest_sock.close()
                return False
    
    def get_response(self, request):
        
        cmd = [request.header.get_protocol_command()]
         
        if request.header.options is not None:
            cmd.append(str(request.header.options))

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        content = p.stdout.read()
        p.stdout.close()

        msg = Message()
        
        msg.response(request.header, content)
        print msg.content
        return msg
        

if __name__=='__main__':
    argv = sys.argv[1:]
    
    try:
      opts, args = getopt.getopt(argv,'hp:',['help','port='])
    except getopt.GetoptError:
      print 'usage: pyhton daemon [-h, -p port]'
      sys.exit(2)
    print opts
    print args
    
    for opt, arg in opts:
        if opt in ("-p", "--port"):
             try:
                 PORT = int(arg)
             except Exception as e:
                 print 'Numero de porta invalido'
    
    print 'Listening on port ' + str(PORT)
	
    # Socket utilizado pela maquina para se conectar com o backend
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))

    threads = list()

    while True:
        sock.listen(5)
        (dest_sock, (ip, port)) = sock.accept()
        dest_sock.settimeout(60)
        t = Daemon(ip, port, dest_sock)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

'''import subprocess

send = Message()

send.request('127.0.0.1','ps', 'aux', 1) 

request = Message()

encoded = send.encode()
encoded.seek(0)

request.decode(encoded)

print request.header.protocol
print request.header.options

get = Message()

if request.header.protocol == 1:
    cmd = ['ps']
else:
    cmd = ['ls']

print str(request.header.options)

cmd.append(str(request.header.options))
#cmd.append('aux')
content = subprocess.check_output(cmd)
get.response(request.header,content)

pkt = get.encode()
pkt.seek(0)
g = open('teste', 'wb')

g.write(pkt.read())

'''
