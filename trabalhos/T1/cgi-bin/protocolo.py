import io
import re
import struct
from socket import inet_aton
from socket import inet_ntoa

class Header:

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
        return  'Version: ' + str(self.version) \
              + '\nIHL: ' + str(self.ihl) \
              + '\nTotal Length: ' + str(self.total_length) \
              + '\nID: ' + str(self.id) \
              + '\nFlags: ' + str(self.flags) \
              + '\nTTL: ' + str(self.ttl) \
              + '\nProtocol: ' + str(self.protocol) \
              + '\nHeader Checksum: ' + str(self.hc) \
              + '\nSource: ' + inet_ntoa(self.src) \
              + '\nDestination: ' + inet_ntoa(self.dest) \
              + '\nOptions: ' + str(self.options) 

    def decode(self, packet):
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
            
            nro_options = self.ihl - 5

            self.options = packet.read(nro_options * 4)
            self.options = re.sub(b'\x00', '', self.options)

        except Exception as e:
            print e

    def encode(self):
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
                for i in range(0, padding_size):
                    header_bytes.write(struct.pack('B', 0))

        return header_bytes
     
    def setup(self, size_content):
        self.ihl = 5
        
        if self.options is not None:
            self.ihl = self.ihl + len(self.options)//4

            if (len(self.options) % 4) > 0:
                self.ihl = self.ihl + 1

        self.total_length = (self.ihl * 4) + size_content


class Message:
    
    def __init__(self):
        self.header = Header()
        self.content = None

    def decode(self, packet):
        # Faz a decodificacao dos primeiros bytes do cabecalho
        self.header.decode(packet)
        # Como o cabecalho foi consumido, o restante e conteudo
        self.content = packet.read()
    
    def request(self, addr, args, id_request, ttl=10):
        self.header.id = id_request

        self.header.ttl = ttl

        self.header.flags = 0
 
        cmd = args[0]
        if cmd == 'ps':
            self.header.protocol = 1
        elif cmd == 'df':
            self.header.protocol = 2
        elif cmd == 'finger':
            self.header.protocol = 3
        elif cmd == 'uptime':
            self.header.protocol = 4
        else:
            return -1

        self.header.src = inet_aton('127.0.0.1')

        self.header.dest = inet_aton(addr)

        self.header.options = ' '.join(args[1:])

        self.header.setup(0)

        return 0
        
    def response(self, header_request, content):
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
        msg_byte = self.header.encode()

        if self.content is not None:
            msg_byte.write(self.content)
        #msg_byte.seek(0)
        return msg_byte


