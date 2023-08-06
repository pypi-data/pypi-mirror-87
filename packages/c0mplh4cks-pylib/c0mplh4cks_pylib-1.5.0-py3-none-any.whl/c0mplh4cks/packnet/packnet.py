"""

 PACKNET  -  c0mplh4cks

 a Packet Constructor and Interpreter


"""





# === Importing Dependencies === #
from struct import pack, unpack
from random import randint
from time import time

from .vendor import vendors







# === Mac Vendor Lookup === #
def maclookup(mac):
    mac = mac.upper().replace(":", "")

    vendor = vendors.get(mac[:6])
    if not vendor:
        vendor = "Unknown vendor"

    return vendor





# === Encode === #
class encode:
    def ip(ip):
        return b"".join( [pack(">B", int(n)) for n in ip.split(".")] )

    def mac(mac):
        return b"".join( [pack(">B", int(n, 16)) for n in mac.split(":")] )





# === Decode === #
class decode:
    def ip(ip):
        return ".".join( [str(n) for n in ip] )

    def mac(mac):
        return ":".join( ["{:02x}".format(n) for n in mac] )







# === Checksum === #
def checksum(header):
    header = b"".join(header)

    if len(header)%2 != 0:
        header += b"\x00"

    values = unpack( f">{ len(header)//2 }H", header )
    n = "{:04x}".format(sum(values))

    while len(n) != 4:
        n = "{:04x}".format( int( n[:len(n)-4], 16 ) + int( n[len(n)-4:], 16 ) )

    return ( 65535 - int(n, 16) )







# === Ethernet === #
class ETHERNET:
    def __init__(self, packet=b""):
        self.packet = packet

        if len(self.packet) >= 14:
            self.read()



    def build(self, src=(), dst=(), protocol=2048, data=b""):
        self.src = src
        self.dst = dst
        self.protocol = protocol
        self.data = data

        packet = [
            encode.mac( dst[2] ),   # Destination MAC
            encode.mac( src[2] ),   # Source MAC
            pack(">H", protocol )   # Protocol/Type
        ]

        packet.append(data)         # Data

        self.packet = b"".join(packet)


        return self.packet



    def read(self):
        packet = self.packet

        self.src = ( "", 0, decode.mac(packet[6:12]) )
        self.dst = ( "", 0, decode.mac(packet[:6]) )
        self.protocol = unpack( ">H", packet[12:14] )[0]
        self.data = packet[14:]







# === ARP === #
class ARP:
    def __init__(self, packet=b""):
        self.packet = packet

        if len(self.packet) >= 28:
            self.read()



    def build(self, src=(), dst=(), op=1, ht=1, pt=2048, hs=6, ps=4):
        self.src = src
        self.dst = dst
        self.op = op
        self.ht = ht
        self.pt = pt
        self.hs = hs
        self.ps = ps

        packet = [
            pack(">H", 1 ),         # Hardware type
            pack(">H", 2048 ),      # Protocol type
            pack(">B", 6 ),         # Hardware size
            pack(">B", 4 ),         # Protocol size
            pack(">H", op),         # Operation code
            encode.mac( src[2] ),   # Sender MAC
            encode.ip( src[0] ),    # Sender IP
            encode.mac( dst[2] ),   # Target MAC
            encode.ip( dst[0] ),    # Target IP
        ]

        self.packet = b"".join(packet)


        return self.packet



    def read(self):
        packet = self.packet

        self.src = ( decode.ip(packet[14:18]), 0, decode.mac(packet[8:14]) )
        self.dst = ( decode.ip(packet[24:28]), 0, decode.mac(packet[18:24]) )
        self.op = unpack( ">H", packet[6:8] )[0]
        self.ht = unpack( ">H", packet[:2] )[0]
        self.pt = unpack( ">H", packet[2:4] )[0]
        self.hs = packet[4]
        self.ps = packet[5]







# === IPv4 === #
class IPv4:
    def __init__(self, packet=b""):
        self.packet = packet

        if len(self.packet) >= 20:
            self.read()



    def build(self, src=(), dst=(), protocol=17, id=0, dscp=0, vhl=69, flags=16384, ttl=64, data=b""):
        self.src = src
        self.dst = dst
        self.protocol = protocol
        self.id = id
        self.dscp = dscp
        self.vhl = vhl
        self.flags = flags
        self.ttl = ttl
        self.data = data

        packet = [
            pack(">B", vhl ),               # Version & Header length
            pack(">B", dscp ),              # Differentiated services field
            pack(">H", 20+len(data) ),      # Total length
            pack(">H", id ),                # Identification
            pack(">H", flags ),             # Flags
            pack(">B", ttl ),               # Time to live
            pack(">B", protocol ),          # Protocol

            encode.ip( src[0] ),            # Source IP
            encode.ip( dst[0] ),            # Destinaction IP
        ]

        packet.insert( 7, pack(">H", checksum(packet)) )    # Checksum
        packet.append(data)                                 # Data

        self.packet = b"".join(packet)


        return self.packet



    def read(self):
        packet = self.packet

        self.src = ( decode.ip(packet[:]), 0, "" )
        self.dst = ( decode.ip(packet[:]), 0, "" )
        self.protocol = unpack(">H", packet[2:4] )[0]
        self.id = unpack(">H", packet[4:6] )[0]
        self.dscp = packet[1]
        self.vhl = packet[0]
        self.flags = unpack(">H", packet[6:8] )[0]
        self.ttl = packet[8]
        self.data = packet[9]
