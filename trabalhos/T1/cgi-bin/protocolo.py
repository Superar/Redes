import io
import re
import struct
from socket import inet_aton
from socket import inet_ntoa
from socket import gethostbyname
from socket import gethostname

COMANDO_DICT = {'ps':1,
                'df':2,
                'finger':3,
                'uptime':4}

MIN_TAM_HEADER = 20 # 20 bytes

class Header(object):
    """ Classe que representa o cabecalho de um pacote.
    O cabecalho contem diversos campos. Os tamanhos em bits e os
    conteudos estao especificados no construtor abaixo
    """

    def __init__(self):
        # Version (4 bits)
        self.version = 2
        # IHL (4 bits)
        self.ihl = 5 # 5 + tamanho options em words
        # Type Of Service (8 bits)
        self.tos = 0
        # Total Length (16 bits)
        self.total_length = 4 * self.ihl # tamanho do cabecalho + conteudo
        # Identification (16 bits)
        self.id = 0
        # Flags (3 bits)
        self.flags = 0
        # Fragment Offset (13 bits)
        self.fo = 0
        # Time to Live (8 bits)
        self.ttl = 0
        # Protocol (8 bits)
        self.protocol = 0
        # Header Checksum (16 bits)
        self.hc = 0
        # Source Address (32 bits)
        self.src = None
        # Destination Address (32 bits)
        self.dest = None
        # Options (x bits)
        self.options = None

    def __str__(self):
        ''' Metodo para conversao do header para string.
        Facilita leitura e impressao do cebecalho
        '''

        src_addr = 'None' if self.src is None else inet_ntoa(self.src)
        dest_addr = 'None' if self.dest is None else inet_ntoa(self.dest)
        return  'Version: ' + str(self.version) \
              + '\nIHL: ' + str(self.ihl) \
              + '\nTotal Length: ' + str(self.total_length) \
              + '\nID: ' + str(self.id) \
              + '\nFlags: ' + str(self.flags) \
              + '\nTTL: ' + str(self.ttl) \
              + '\nProtocol: ' + str(self.protocol) \
              + '\nHeader Checksum: ' + str(self.hc) \
              + '\nSource: ' + src_addr \
              + '\nDestination: ' + dest_addr \
              + '\nOptions: ' + str(self.options)

    def decode(self, packet):
        ''' Decodificacao de um pacote binario.
            Dado um ``packet`` em binario, decodifica-o inicializando os campos do cabecalho
        '''

        try:
            word = struct.unpack('!HH', packet.read(4))
            field = word[0] >> 8

            self.version = field >> 4
            self.ihl = field & 0x0f
            self.total_length = word[1]

            word = struct.unpack('!HH', packet.read(4))

            self.id = word[0]
            self.flags = word[1] >> 13

            word = struct.unpack('!HH', packet.read(4))

            self.ttl = word[0] >> 8
            self.protocol = word[0] & 0x00FF
            self.hc = word[1]

            self.src = packet.read(4)
            self.dest = packet.read(4)

            self.set_options(packet)

        except Exception as e:
            print e

    def set_options(self, data):
        self.options = data.read((self.ihl - 5) * 4)
        self.options = re.sub(b'\x00', '', self.options)

    def encode(self):
        ''' Codificacao do cabecalho em uma estrutura de bits.

            Codifica os campos do cabecalho no formato de especificacao do cabecalho em binario
            Retorna o cabecalho em binario
        '''

        header_bytes = io.BytesIO()

        byte = ((self.version << 4) | self.ihl) << 8
        header_bytes.write(struct.pack('!H', byte))

        header_bytes.write(struct.pack('!H', self.total_length))

        header_bytes.write(struct.pack('!H', self.id))

        header_bytes.write(struct.pack('!H', self.flags << 13))

        byte = (self.ttl << 8) | self.protocol
        header_bytes.write(struct.pack('!H', byte))

        header_bytes.write(struct.pack('!H', self.hc))

        header_bytes.write(self.src)

        header_bytes.write(self.dest)

        if self.options is not None:
            padding_size = 4 - (len(self.options) % 4)

            header_bytes.write(self.options)

            if padding_size < 4:
                for _ in range(0, padding_size):
                    header_bytes.write(struct.pack('B', 0))

        return header_bytes

    def get_header_checksum(self):
        ''' Calculo do cecksum do cabecalho.

            Checksum eh a soma de todos os bits presentes no cabecalho.
            Caso haja um carry no resultado, este bit deve ser removido e somado
            ao resultado, permitindo que o checksum possua 16 bits.
        '''

        hc = ((self.version << 4) | self.ihl) << 8

        hc = hc + (self.total_length)

        hc = hc + self.id

        hc = hc + (self.flags << 13)

        hc = hc + ((self.ttl << 8) | self.protocol)

        sum_addr = 0
        for i in range(0, 4, 2):
            byte = struct.unpack('!H', self.src[i] + self.src[i + 1])[0]
            sum_addr = sum_addr + byte

            byte = struct.unpack('!H', self.dest[i] + self.dest[i + 1])[0]
            sum_addr = sum_addr + byte

        hc = hc + sum_addr

        if self.options is not None:

            for i in range(0, len(self.options) - 1, 2):
                byte = struct.unpack('!H', self.options[i] + self.options[i+1])[0]
                hc = hc + byte

            if (len(self.options) - 2) > i:
                byte = struct.unpack('!H', self.options[i + 2] + '\x00')[0]
                hc = hc + byte

        carry = hc >> 16
        hc = (hc & 0xffff) + carry

        return hc

    def setup(self, size_content):
        ''' Configura os campos calculados (ihl, length, hc)
        com os valores especificados em seus campos
        '''

        self.ihl = 5
        if self.options is not None:
            self.ihl = self.ihl + len(self.options)//4

            if (len(self.options) % 4) > 0:
                self.ihl = self.ihl + 1
        self.total_length = (self.ihl * 4) + size_content
        self.hc = self.get_header_checksum()

    def get_protocol_command(self):
        ''' Decodifica o campo protocolo e retorna o nome do comando que representa '''

        dict_contrario = dict(zip(COMANDO_DICT.values(), COMANDO_DICT.keys()))
        return dict_contrario[self.protocol]

class Message(object):
    ''' Classe que representa uma mensagem a ser enviada.

    Atributos:
    ``header`` - Cabecalho da mensagem
    ``content`` - Conteudo da mensagem
    '''

    def __init__(self):
        self.header = Header()
        self.content = None

    def decode(self, packet):
        ''' Decodifica um apanhado de bytes em um objeto Message '''

        # Faz a decodificacao dos primeiros bytes do cabecalho
        self.header.decode(packet)
        # Como o cabecalho foi consumido, o restante e conteudo
        self.content = packet.read()

    # Monta um pacote de requisicao de um comando
    def request(self, addr, args, id_request, ttl=10):
        ''' Monta um pacote de requisicao de um comando.

        ``addr`` - Endereco a ser enviado o pacote
        ``args`` - Argumentos do comando. Primeira posicao indica o nome do comando
        ``id_request`` - Identificador do comando
        ``ttl`` - Tempo de vida do pacote
        '''

        self.header.id = id_request

        self.header.ttl = ttl

        self.header.flags = 0

        self.header.protocol = COMANDO_DICT[args[0]]

        self.header.src = inet_aton(gethostbyname(gethostname()))

        self.header.dest = inet_aton(addr)

        self.header.options = ' '.join(args[1:])

        self.header.setup(0)

        return 0

    def response(self, header_request, content):
        ''' Monta um pacote de resposta a uma requisicao.

        ``header_request`` - Cabecalho da requisicao a ser respondida
        ``content`` - Conteudo da resposta. No caso, a saida da execucao do programa.
        '''

        self.header.id = header_request.id
        self.header.ttl = header_request.ttl - 1

        self.header.flags = 7 # 111

        self.header.protocol = header_request.protocol

        self.header.src = header_request.dest

        self.header.dest = header_request.src

        self.content = content
        self.header.setup(len(content))
        return 0

    def encode(self):
        ''' Codifica os atributos da Message em um conjunto de bytes '''

        msg_bytes = self.header.encode()

        if self.content is not None:
            msg_bytes.write(self.content)
        return msg_bytes

    def send_only(self, sock):
        ''' Apenas envia os dados para ``sock``, sem esperar uma resposta '''

        data = self.encode()
        data.seek(0)
        # Envio dos dados
        try:
            sock.sendall()
        except Exception as e:
            print 'Falha no envio:'
            print e
            raise RuntimeError('Falha no envio de pacote')

    def send(self, sock):
        ''' Envia os dados para ``sock`` e recebe a resposta logo em seguida '''

        self.send_only(sock)

        response = Message.recv(sock)

        hc = response.header.hc - response.header.get_header_checksum()

        if (hc == 0) and (response.header.id == self.header.id):
            return response
        else:
            response.content = 'Pacote invalido'
            response.header.setup(len(response.content))
            return response


    @classmethod
    def recv(cls, sock):
        ''' Recebe os dados pelo socket e monta uma mensagem com estes dados '''

        response = None
        # Recebe o cabecalho para verificar a quantidade de dados que falta
        header_response = sock.recv(20)


        if len(header_response) > 0:
            buf = io.BytesIO(header_response)
            header = Header()
            header.decode(buf)


            response = cls()
            response.header = header

            if header.total_length > 20:
                data_response = sock.recv(header.total_length - 20)
                buf = io.BytesIO(data_response)
                response.header.set_options(buf)
                response.content = buf.read()

        return response
