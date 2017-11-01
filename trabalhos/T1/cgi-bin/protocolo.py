import io
import struct

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
        self.tl = 0
        # Protocol (8 bits)
        self.protocol = 0
        # Header Checksum (16 bits)
        self.hc = 0
        # Source Address (32 bits)
        self.src = 0
        # Destination Address (32 bits)
        self.dest = 0
        # Options (x bits)
        self.options = 0

    def set_content_length(self, length):
        self.total_lenght = self.ihl + lenght

    def set_flags(self, flags):
        self.flags = flags

    def set_tl(self, time):
        self.tl = time

    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_src(self, src):
        self.src = src
    
    def set_dest(self, dest):
        self.dest = dest

    def set_options(self, options):
        self.options = options
    
    def decode_header(self, packet):
       try:
        word = struct.unpack('!HH', packet.read(4))
        field = word[0] >> 8
       
        self.version = field >> 4
        print self.version
        self.ihl = field & 0x0f
        print self.ihl
        self.total_length = word[1]
        print self.total_length
        
        word = struct.unpack('!HH', packet.read(4))
        
        self.id = word[0]
        print self.id
        self.flags = word[1] >> 13
        print self.flags

        word = struct.unpack('!HH', packet.read(4))
        
        self.tl = word[0] >> 8
        print self.tl
        self.protocol = word[0] & 0x00FF
        print self.protocol
        self.hc = word[1]
        print self.hc
        
        word = struct.unpack('!II', packet.read(8))
       
        print 'enderecos'
        self.src = word[0]
        print self.src
        self.dest = word[1]
        print self.dest
        nro_options = self.ihl - 5

        self.options = packet.read(nro_options * 4)
        print self.options
       except Exception as e:
        print e

class Packet:
    
    def __init__(self):
        self.header = Header()
        self.content = 0

    def decode_packet(self, packet):
        self.content = self.header.decode_header(packet)
        print packet.read(5)

f = open('header_example', 'rb')

b = io.BytesIO(f.read())

b.seek(0)

p = Packet()

p.decode_packet(b)
