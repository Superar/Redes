import socket
import threading


HOST = '0.0.0.0'
PORT = 9999


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
                data = self.dest_sock.recv(tam)

                if data:
                    self.dest_sock.send(data)
                else:
                    raise error('Desconectado')
            except:
                self.dest_sock.close()
                return False


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

