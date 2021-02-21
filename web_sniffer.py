#!/usr/bin/python3

from scapy.all import *

def packet_callback(packet):
    print("Packet handler started...")
    if packet["TCP"].payload:
        web_packet = str(packet["TCP"].payload)

        if "sniff_success" in web_packet:
            print("SRC: %s\nDST: %s\n-----------\n" % (packet["IP"].src,
                                                       packet["IP"].dst))
            print(web_packet)

            
    
print("Sniffer running...")
while True:
    sniff(filter="tcp port 80", prn=packet_callback, store=0)
