"""

 PACKNET  -  c0mplh4cks

 UDP


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode, checksum







# === UDP === #
class UDP:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.length = 0
        self.checksum = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 8 + len(self.data)

        packet.insert(0, pack( ">H", self.src[1] ))     # Source PORT
        packet.insert(1, pack( ">H", self.dst[1] ))     # Target PORT
        packet.insert(2, pack( ">H", self.length ))     # Total length
        packet.insert(4, self.data)                     # Data
        packet.insert(3, checksum( [                    # Checksum
            *packet,
            encode.ip( self.src[0] ),
            encode.ip( self.dst[0] ),
            pack( ">H", 17 ),
            pack( ">H", self.length )
        ] ))

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.src[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Source PORT
        i, self.dst[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Target PORT
        i, length           = i+2, unpack( ">H", packet[i:i+2] )[0]     # Total length
        i, self.checksum    = i+2, unpack( ">H", packet[i:i+2] )[0]     # Checksum
        i, self.data        = i+len( packet[i:] ), packet[i:]           # Data

        self.length = i

        return i
