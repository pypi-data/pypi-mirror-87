"""

 PACKNET  -  c0mplh4cks

 INTERFACE


"""





# === Importing Dependencies === #
import socket
from .standards import encode, decode







# === Interface === #
class Interface():
    def __init__(self, card=None, port=0, passive=False):

        self.sock = socket.socket( socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003) )


        if not card:
            self.card = [ i[1] for i in socket.if_namei() ][-1]
        else:
            self.card = card

        if not passive:
            s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            s.setsockopt( socket.SOL_SOCKET, 25, f"{ self.card }".encode() )
            s.connect( ("1.1.1.1", 80) )
            ip = s.getsockname()[0]

            self.sock.bind( (self.card, 0) )
            mac = decode.mac( self.sock.getsockname()[4] )

            self.addr = ( ip, port, mac )


    def send(self, packet):
        self.sock.send(packet)

    def recv(self, length=1024):
        return self.sock.recvfrom(length)
