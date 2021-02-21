#!/usr/bin/python
import os, socket
import struct
from ctypes import *
import sys

#import hexdump


HOST="192.168.123.100"

#IP HEADER
class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),       #header length   [0][4:7]
        ("ver", c_ubyte, 4),    #version         [0][0:3] 
        ("tos", c_ubyte, 8),          #type of service [0][8:15]    
        ("len", c_ushort, 16),         #header+data length   [0][16:31]  
        ("id", c_ushort, 16),          #id              [32][0:15]  
        ("offset", c_ushort, 16),      #offset          [32][16:31]
        ("ttl", c_ubyte, 8),          #time to live    [64][0:7]
        ("p_num", c_ubyte, 8), #protocol num    [64][8:15]
        ("sum", c_ushort, 16),         #header checksum [64][16:31]
        ("src", c_ulong, 32),          #source IP addr  [96][0:31]
        ("dst", c_ulong, 32)           #dest IP addr    [128][0:31]
        #("pad1", c_ulonglong),
        #("pad2", c_ulong)
    ]

    def __new__(self, sock_buf=None):
        print("making instance...")
        #temp_buf =  sock_buf + (b"\x00" * 12)
        
        return self.from_buffer_copy(sock_buf) #ERROR: struct size must be wrong! 20 into 32

    def __init__(self, sock_buf=None):
        print("Parsing header...")

        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
        
        #pack src into little-endian(<) + unsigned-long(L) format 
        #alt: self.src_addr = struct.pack("!L", self.src)
        #self.src_addr = socket.inet_ntoa(struct.pack("<L",self.src))
        self.src_addr = socket.inet_ntoa(struct.pack("<L",self.src))
        
        #pack dst into little-endian(<) + unsigned-long(L) format
        #alt: self.dst_addr = struct.pack("!L", self.dst)
        self.dst_addr = socket.inet_ntoa(struct.pack("<L", self.dst))

        
        try:
            self.protocol = self.protocol_map[self.p_num]
        except:
            self.protocol = str(self.p_num)

    def printall(self):
        return
    
def main():
    print("packet sniffer from BHP....")

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sniffer.bind(("192.168.123.100", 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    try:


        
        while True: 
            raw_buf = sniffer.recvfrom(1508)[0] #[0]: data, [1]:ret_addr
            print("Received packet:") 
            
            #ip_header = object.__new__(IP)
            #IP.__init__(ip_header, raw_buf[0:20])
            ip_header = IP(raw_buf[0:32]) #first 20 bytes
            print(raw_buf[0:32])
            print("Protocol: %s\nSRC: %s\nDST: %s" % (ip_header.protocol,
                                                      ip_header.src_addr,
                                                      ip_header.dst_addr))
            
            #for field in IP._fields_:
                #print("%s: %s" % (field[0], ip_header.field[0]))
            
    except Exception as e:
        print(e)
    
if __name__=="__main__":
    main()
    
    
    
    
