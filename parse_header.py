#!/usr/bin/python3
import socket, struct, binascii

LHOST="0.0.0.0"
LPORT=0

class ETHERNET_HEADER:
    def __init__(self, b_header):
        eth_header = struct.unpack("!6s6s2s", b_header)

        self.dst_mac = binascii.hexlify(eth_header[0])
        self.src_mac = binascii.hexlify(eth_header[1])
        self.eth_type = binascii.hexlify(eth_header[2])     
               
class IP_HEADER:
    def __init__(self, b_header):
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        ip_header = struct.unpack("!BBHHHBBH4s4s", b_header)

        self.ver_ihl = ip_header[0]
        #self.ver = format(self.ver_ihl, "b")[0:3]
        #self.ihl = format(self.ver_ihl, "b")[4:7]
        self.tos = ip_header[1]
        self.len = ip_header[2]
        self.id = ip_header[3]
        self.offset = ip_header[4]
        self.ttl = ip_header[5]
        self.protocol_num = ip_header[6]
        self.protocol = self.protocol_map[ip_header[6]]
        self.checksum = ip_header[7]
        self.src_addr = socket.inet_ntoa(ip_header[8])
        self.dst_addr = socket.inet_ntoa(ip_header[9])

#        self.ver = "0000" + format(self.ver_ihl, "b")[0:3]
 #       self.ver = "0000" + format(self.ver_ihl, "b")[4:7] 
            


def main():
    print("packet sniffer by dks...")

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) # IPPROTO_IP == socket.htons(0x0800)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    while True:
        packet = s.recvfrom(65565)
        print("packet recieved")

        #eth_header = ETHERNET_HEADER(packet[0][0:14])
        ip_header = IP_HEADER(packet[0][0:20])

        print("PROTOCOL: %s\nSRC: %s\nDST: %s\n" % (ip_header.protocol,
                                                    ip_header.src_addr,
                                                    ip_header.dst_addr))
                                                    
                                                    


if __name__=="__main__":
    main()
