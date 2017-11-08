import socket
import threading
import sys
import getopt
import subprocess
from protocolo import *

# Definicao do localhost
HOST = '127.0.0.1'
# Definicao da porta padrao
PORT = 9001

class Daemon(threading.Thread):
    ''' Classe representante de um Daemon
        O Daemon deve receber um pacote conforme especificado no arquivo protocolo.py,
        executar os comandos necessarios e enviar a resposta com o resultado da execucao
        do comando
    '''

    # Cria a thread de conexao com ip, porta e o socket para resposta
    def __init__(self, ip, port, sock):
        ''' Construtor. Inicia a Thread
            e inicializa as configuracoes do socket do cliente
            (de onde recebera e para onde enviara os pacotes)
        '''
 
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.dest_sock = sock

    # Execucao da thread
    def run(self):
        ''' Codigo a ser executado pela Thread.
            O codigo deve receber um pacote de dados da conexao aberta,
            decodifica-lo, executar o comando com os parametros indicados
            e enviar pela mesma conexao o pacote com a saida do comando indicado
        '''

        while True:
            try:
                # Recebe os dados atraves do socket
                request = Message.recv(self.dest_sock)

                # Se recebeu dados dados
                if request & request.flags == 0:
                    # Gera a resposta correspondente
                    response = self.get_response(request)            
                    
                    # Apenas envia a resposta da requisicao
                    response.send_only(self.dest_sock)
                else:
                    # Backend mandou um shutdown
                    self.dest_sock.close()
                    raise error('Desconectado')
            except:
                self.dest_sock.close()
                return False
    
    def get_response(self, request):
        ''' Executa comandos em um sub-processo
            De acordo com uma requisicao recebida em um pacote conforme indicado
            em protocolo.py
        '''
        # Cria lista com nome do comando a ser executado e argumentos
        cmd = [request.header.get_protocol_command()]
        if request.header.options is not None and len(request.header.options) > 0:
           cmd.append(str(request.header.options))

        # Abre um sub-processo e executa o comando
        # Armazenando as saidas de stdout e stderr
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        content = p.stdout.read()
        erro = p.stderr.read()
        p.stdout.close()
        p.stderr.close()

        # Saida com erro
        if len(content) == 0:
            content = erro

        # Retorna a saida de execucao
        msg = Message()
        msg.response(request.header, content)
        return msg
        

if __name__=='__main__':
    argv = sys.argv[1:]
   
    # Tratamento das opcoes na inicializacao do daemon em linha de comando
    # Argumento indica a porta a ser utilizada 
    try:
      opts, args = getopt.getopt(argv,'hp:',['help','port='])
    except getopt.GetoptError:
      print 'usage: pyhton daemon [-h, -p port]'
      sys.exit(2)
    
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
    sock.bind(('localhost', PORT))

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
