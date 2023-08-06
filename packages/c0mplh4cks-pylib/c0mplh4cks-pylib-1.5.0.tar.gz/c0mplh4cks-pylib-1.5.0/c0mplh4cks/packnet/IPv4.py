"""

 PACKNET  -  c0mplh4cks

 IPV4


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode, checksum







# === IPv4 === #
class IPv4:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.protocol = 17
        self.id = 0
        self.dscp = 0
        self.vhl = 69
        self.flags = 0b010
        self.ttl = 64
        self.length = 0
        self.checksum = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 20 + len(self.data)

        packet.insert(0, pack( ">B", self.vhl ))            # Version & Header length
        packet.insert(1, pack( ">B", self.dscp ))           # Differentiated services field
        packet.insert(2, pack( ">H", self.length ))         # Total length
        packet.insert(3, pack( ">H", self.id ))             # Identification
        packet.insert(4, pack( ">H", self.flags << 13 ))    # Flags
        packet.insert(5, pack( ">B", self.ttl ))            # Time to live
        packet.insert(6, pack( ">B", self.protocol ))       # Protocol
        packet.insert(8, encode.ip( self.src[0] ))          # Source IP
        packet.insert(9, encode.ip( self.dst[0] ))          # Target IP
        packet.insert(7, checksum( packet ))                # Checksum
        packet.insert(10, self.data)                        # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.vhl         = i+1, packet[i]                                # Version & Header length
        i, self.dscp        = i+1, packet[i]                                # Differentiated services field
        i, length           = i+2, unpack( ">H", packet[i:i+2] )[0]         # Total length
        i, self.id          = i+2, unpack( ">H", packet[i:i+2] )[0]         # Identification
        i, self.flags       = i+2, unpack( ">H", packet[i:i+2] )[0] >> 13   # Flags
        i, self.ttl         = i+1, packet[i]                                # Time to live
        i, self.protocol    = i+1, packet[i]                                # Protocol
        i, self.checksum    = i+2, unpack( ">H", packet[i:i+2] )[0]         # Checksum
        i, self.src[0]      = i+4, decode.ip( packet[i:i+4] )               # Source IP
        i, self.dst[0]      = i+4, decode.ip( packet[i:i+4] )               # Target IP
        i, self.data        = i+len( packet[i:] ), packet[i:]               # Data

        self.length = i

        return i
