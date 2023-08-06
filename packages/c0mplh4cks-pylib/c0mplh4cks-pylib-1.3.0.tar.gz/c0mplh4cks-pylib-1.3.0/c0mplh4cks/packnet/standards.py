"""

 PACKNET  -  c0mplh4cks

 STANDARDS


"""





# === Importing Dependencies === #
from struct import pack, unpack
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


    def name(name, header=b""):
        encoded = b""
        for label in f"{ name }.".split("."):
            encoded += ( pack(">B", len(label)) + label.encode() )

        pointer = header.find(encoded)
        if pointer == -1:
            return encoded
        else:
            return pack(">H", 49152+pointer )






# === Decode === #
class decode:
    def ip(ip):
        return ".".join( [str(n) for n in ip] )


    def mac(mac):
        return ":".join( ["{:02x}".format(n) for n in mac] )


    def name(name, header=b"", ti=0):
        labels = []
        i = 0

        while True:
            length = name[i]

            if length == 0:
                break

            elif (length >> 6) == 3:
                pointer = unpack(">H", name[i:i+2] )[0] -49152
                i += 2
                name = name[:i] + header[pointer:] + name[i:]

            else:
                i += 1
                labels.append( name[ i:length+i ].decode() )
                i += length

        name = ".".join( labels )

        return i+ti+1, name







# === Checksum === #
def checksum(header):
        header = b"".join(header)

        if (len(header) %2) != 0:
            header += b"\x00"

        values = unpack( f">{ len(header)//2 }H", header )
        n = sum(values) %65535
        n = 65535-n

        return pack(">H", n )
