"""

 PACKNET  -  c0mplh4cks

 DNS


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode







# === DNS === #
class DNS:
    def __init__(self, packet=b""):
        self.packet = packet

        self.id = 0
        self.flags = 0b000000100
        self.question = []
        self.answer = []
        self.authority = []
        self.additional = []
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        for section in (self.question, self.answer, self.authority, self.additional):
            for record in section:
                record.build()
                self.data += record.packet

        self.length = 12 + len(self.data)

        packet.insert(0, pack( ">H", self.id ))                 # Transaction ID
        packet.insert(1, pack( ">H", self.flags << 4 ))         # Flags
        packet.insert(2, pack( ">H", len(self.question) ))      # Questions
        packet.insert(3, pack( ">H", len(self.answer) ))        # Answer RRs
        packet.insert(4, pack( ">H", len(self.authority) ))     # Authority RRs
        packet.insert(5, pack( ">H", len(self.additional) ))    # Additional RRs
        packet.insert(6, self.data )                            # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.id      = i+2, unpack( ">H", packet[i:i+2] )[0]         # Transaction ID
        i, self.flags   = i+2, unpack( ">H", packet[i:i+2] )[0] >> 4    # Flags
        i, questions    = i+2, unpack( ">H", packet[i:i+2] )[0]         # Questions
        i, answers      = i+2, unpack( ">H", packet[i:i+2] )[0]         # Answer RRs
        i, authoritys   = i+2, unpack( ">H", packet[i:i+2] )[0]         # Authority RRs
        i, additionals  = i+2, unpack( ">H", packet[i:i+2] )[0]         # Additional RRs
        i, self.data    = i, packet[i:]                                 # Data

        for j in range(questions):                                              # Question data
            query = Query( self.packet[i:], self.packet )
            i += query.read()
            self.question.append(query)

        for j in range(answers):                                                # Answer data
            answer = Answer( self.packet[i:], self.packet )
            i += answer.read()
            self.answer.append(answer)

        self.length = i

        return i







# === Query === #
class Query:
    def __init__(self, packet=b"", header=b""):
        self.packet = packet
        self.header = header

        self.name = ""
        self.type = 5
        self.classif = 1
        self.length = 0



    def build(self):
        packet = []

        name = encode.name( self.name, self.header )

        self.length = 4 + len(name)

        packet.insert(0, name )                         # Name
        packet.insert(1, pack( ">H", self.type ))       # Type
        packet.insert(2, pack( ">H", self.classif ))    # Class

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.name    = decode.name( packet[i:], self.header, i )     # Name
        i, self.type    = i+2, unpack( ">H", packet[i:i+2] )[0]         # Type
        i, self.classif = i+2, unpack( ">H", packet[i:i+2] )[0]         # Class

        self.length = i

        return i







# === Answer === #
class Answer:
    def __init__(self, packet=b"", header=b""):
        self.packet = packet
        self.header = header

        self.name = ""
        self.type = 1
        self.classif = 1
        self.ttl = 64
        self.cname = ""
        self.length = 0



    def build(self):
        packet = []

        name = encode.name( self.name, self.header)
        if self.type == 1:
            cname = encode.ip( self.cname )
        elif self.type != 1:
            cname = encode.name( self.cname, self.header)

        self.length = 10 + len(name) + len(cname)

        packet.insert(0, name)                          # Name
        packet.insert(1, pack( ">H", self.type ))       # Type
        packet.insert(2, pack( ">H", self.classif ))    # Class
        packet.insert(3, pack( ">L", self.ttl ))        # Time to live
        packet.insert(4, pack( ">H", self.length ))     # Total Length
        packet.insert(5, cname)                         # Cname

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.name    = decode.name( packet[i:], self.header, i )     # Name
        i, self.type    = i+2, unpack( ">H", packet[i:i+2] )[0]         # Type
        i, self.classif = i+2, unpack( ">H", packet[i:i+2] )[0]         # Class
        i, self.ttl     = i+4, unpack( ">L", packet[i:i+4] )[0]         # Time to live
        i, length       = i+2, unpack( ">H", packet[i:i+2] )[0]         # Total Length

        if self.type == 1:                                              # Cname
            i, self.cname = i+4, decode.ip( packet[i:] )
        elif self.type != 1:
            i, self.cname   = decode.name( packet[i:], self.header, i )

        self.length = i

        return i
