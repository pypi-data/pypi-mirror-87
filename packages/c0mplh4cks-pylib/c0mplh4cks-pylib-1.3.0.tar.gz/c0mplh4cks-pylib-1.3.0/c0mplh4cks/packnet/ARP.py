"""

 PACKNET  -  c0mplh4cks

 ARP


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode







# === ARP === #
class ARP:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.op = 1
        self.ht = 1
        self.pt = 2048
        self.hs = 6
        self.ps = 4
        self.length = 0



    def build(self):
        packet = []

        self.length = 28

        packet.insert(0, pack( ">H", self.ht ))         # Hardware type
        packet.insert(1, pack( ">H", self.pt ))         # Protocol type
        packet.insert(2, pack( ">B", self.hs ))         # Hardware size
        packet.insert(3, pack( ">B", self.ps ))         # Protocol size
        packet.insert(4, pack( ">H", self.op ))         # Operation code
        packet.insert(5, encode.mac( self.src[2] ))     # Source MAC
        packet.insert(6, encode.ip( self.src[0] ))      # Source IP
        packet.insert(7, encode.mac( self.dst[2] ))     # Target MAC
        packet.insert(8, encode.ip( self.dst[0] ))      # Target IP

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.ht      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Hardware type
        i, self.pt      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Protocol type
        i, self.hs      = i+1, packet[i]                            # Hardware size
        i, self.ps      = i+1, packet[i]                            # Protocol size
        i, self.op      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Operation code
        i, self.src[2]  = i+6, decode.mac( packet[i:i+6] )          # Source MAC
        i, self.src[0]  = i+4, decode.ip( packet[i:i+4] )           # Source IP
        i, self.dst[2]  = i+6, decode.mac( packet[i:i+6] )          # Target MAC
        i, self.dst[0]  = i+4, decode.ip( packet[i:i+4] )           # Target IP

        self.length = i

        return i
