"""

 PACKNET  -  c0mplh4cks

 ICMP


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode, checksum







# === ICMP === #
class ICMP:
    def __init__(self, packet=b""):
        self.packet = packet

        self.type = 0
        self.code = 0
        self.checksum = 0
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 4 + len(self.data)

        packet.insert(0, pack( ">B", self.type ))       # Type
        packet.insert(1, pack( ">B", self.code ))       # Code
        packet.insert(3, self.data )                    # Checksum
        packet.insert(2, checksum( packet ))            # Packet

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.type        = i+1, packet[i]                            # Type
        i, self.code        = i+1, packet[i]                            # Code
        i, self.checksum    = i+2, unpack( ">H", packet[i:i+2] )[0]     # Checksum
        i, self.data        = i+len( packet[i:]), packet[i:]            # Data

        self.length = i

        return i







# === Echo === #
class Echo:
    def __init__(self, packet=b""):
        self.packet = packet

        self.id = 0
        self.seq = 0
        self.timestamp = 0
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 12 + len(self.data)

        packet.insert(0, pack( ">H", self.id ))             # Identifier
        packet.insert(1, pack( ">H", self.seq ))            # Sequence number
        packet.insert(2, pack( "<Q", self.timestamp ))      # Timestamp
        packet.insert(3, self.data )                        # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.id          = i+2, unpack( ">H", packet[i:i+2] )[0]     # Identifier
        i, self.seq         = i+2, unpack( ">H", packet[i:i+2] )[0]     # Sequence number
        i, self.timestamp   = i+8, unpack( "<Q", packet[i:i+8] )[0]     # Timestamp
        i, self.data        = i+len( packet[i:] ), packet[i:]           # Data

        self.length = i

        return i







# === Time Exceeded === #
class TimeExceeded:
    def __init__(self, packet=b""):
        self.packet = packet

        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 4 + len(self.data)

        packet.insert(0, pack( ">L", 0 ))       # Unused
        packet.insert(1, self.data )            # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, unused       = i+4, unpack( ">L", packet[i:i+4] )[0]     # Unused
        i, self.data    = i+len( packet[i:] ), packet[i:]           # Data

        self.length = i

        return i
