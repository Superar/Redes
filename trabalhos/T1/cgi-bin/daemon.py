import socket
import threading
import sys
import getopt

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
                
                # Se houve dados
                if data:
                    self.dest_sock.send(data)
                else:
                    raise error('Desconectado')
            except:
                self.dest_sock.close()
                return False


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
