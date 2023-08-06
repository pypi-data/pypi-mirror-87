"""

 PACKNET  -  c0mplh4cks

 ETHERNET


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode







# === Ethernet === #
class ETHERNET:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.protocol = 2048
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 14 + len(self.data)

        packet.insert(0, encode.mac( self.dst[2] ))     # Target MAC
        packet.insert(1, encode.mac( self.src[2] ))     # Source MAC
        packet.insert(2, pack( ">H", self.protocol ))   # Protocol
        packet.insert(3, self.data)                     # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.dst[2]      = i+6, decode.mac( packet[i:i+6] )          # Target MAC
        i, self.src[2]      = i+6, decode.mac( packet[i:i+6] )          # Source MAC
        i, self.protocol    = i+2, unpack( ">H", packet[i:i+2] )[0]     # Protocol
        i, self.data        = i+len( packet[i:] ), packet[i:]           # Data

        self.length = i

        return i
