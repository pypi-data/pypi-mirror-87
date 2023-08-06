"""

 PACKNET  -  c0mplh4cks

 TCP


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode, checksum







# === TCP === #
class TCP:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.seq = 0
        self.ack = 0
        self.hlength = 0
        self.flags = 0b000000000
        self.win = 65000
        self.urg = 0
        self.length = 0
        self.checksum = 0
        self.options = []
        self.data = b""



    def build(self):
        packet = []

        options = b""
        for option in self.options:
            option.build()
            options += option.packet
        while len(options) %4 != 0:
            options = b"\x01" + options

        self.length = 20 + len(options) + len(self.data)
        self.hlength = (20 + len(options)) // 4
        self.flags += self.hlength << 12

        packet.insert(0, pack( ">H", self.src[1] ))     # Source PORT
        packet.insert(1, pack( ">H", self.dst[1] ))     # Target PORT
        packet.insert(2, pack( ">L", self.seq ))        # Sequence number
        packet.insert(3, pack( ">L", self.ack ))        # Acknowledgement number
        packet.insert(4, pack( ">H", self.flags ))      # Flags
        packet.insert(5, pack( ">H", self.win ))        # Window size
        packet.insert(7, pack( ">H", self.urg ))        # Urgent pointer

        packet.insert(6, checksum( [                    # Checksum
            *packet,
            encode.ip( self.src[0] ),
            encode.ip( self.dst[0] ),
            pack( ">H", 6 ),
            pack( ">H", self.length )
        ] ))

        packet.insert(8, options)                       # Options
        packet.insert(9, self.data )                    # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.src[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Source PORT
        i, self.dst[1]      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Target PORT
        i, self.seq         = i+4, unpack( ">L", packet[i:i+4] )[0]     # Sequence number
        i, self.ack         = i+4, unpack( ">L", packet[i:i+4] )[0]     # Acknowledgement number
        i, self.flags       = i+2, unpack( ">H", packet[i:i+2] )[0]     # Flags & Header length
        i, self.win         = i+2, unpack( ">H", packet[i:i+2] )[0]     # Window size
        i, self.checksum    = i+2, unpack( ">H", packet[i:i+2] )[0]     # Checksum
        i, self.urg         = i+2, unpack( ">H", packet[i:i+2] )[0]     # Urgent pointer

        self.hlength = self.flags >> 12
        self.flags -= self.hlength << 12
        self.hlength = self.hlength * 4

        while i < self.hlength:                                         # Option
            option = Option( packet[i:self.hlength]  )
            i += option.read()
            self.options.append(option)

        i, self.data = i+len( packet[i:] ), packet[i:]                   # Data

        self.length = i

        return i







# === Option === #
class Option:
    def __init__(self, packet=b""):
        self.packet = packet

        self.kind = 0
        self.length = 0
        self.mss = 0
        self.timestamp = 0
        self.timereply = 0
        self.scale = 0
        self.data = b""



    def build(self):
        packet = []

        packet.insert(0, pack( ">B", self.kind ))

        if self.kind == 2:                                  # Maximum segment size
            packet.insert(2, encode.tobyte( self.mss ))
            self.length = len(b"".join(packet)) + 1
            packet.insert(1, pack( ">B", self.length ))

        elif self.kind == 3:                                # Window scale
            packet.insert(2, encode.tobyte( self.scale ))
            self.length = len(b"".join(packet)) + 1
            packet.insert(1, pack( ">B", self.length ))

        elif self.kind == 4:                                # SACK (Selective ACKnowledgement)
            self.length = 2
            packet.insert(1, pack( ">B", self.length ))

        elif self.kind == 8:                                # Timestamps
            self.length = 4
            packet.insert(1, pack( ">B", self.length ))
            packet.insert(2, pack( ">L", self.timestamp ))
            packet.insert(3, pack( ">L", self.timereply ))

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.kind = i+1, unpack( ">B", packet[i:i+1] )[0]

        if self.kind == 2:                                              # Maximum segment size
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.mss = i+(self.length-2), decode.toint( packet[i:i+(self.length-2)] )

        elif self.kind == 3:                                            # Window scale
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.scale = i+(self.length-2), decode.toint( packet[i:i+(self.length-2)] )

        elif self.kind == 4:                                            # SACK (Selective ACKnowledgement)
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.data = i+(self.length-2), packet[i:i+(self.length-2)]

        elif self.kind == 8:                                            # Timestamps
            i, self.length = i+1, unpack( ">B", packet[i:i+1] )[0]
            i, self.timestamp = i+4, unpack( ">L", packet[i:i+4] )[0]
            i, self.timereply = i+4, unpack( ">L", packet[i:i+4] )[0]

        self.length = i

        return i
