#!/usr/bin/python3
import socket
import threading
import sys
import os

RHOST="0.0.0.0"
RPORT=None


def GetArgs():
    global RHOST
    global RPORT

    offset = 0
    for index in range(1, len(sys.argv)):
        arg = sys.argv[index+offset]
    
        if(arg == "-h" or arg == "--help"):
            help()

        elif(arg == "-v" or arg == "-vv"):
            sys.argv.remove(arg)
            offset -= 1
            help()

    if(len(sys.argv) == 3):
        RHOST = sys.argv[1]
        RPORT = int(sys.argv[2])
        
    else:
       print("!!Argument Error!!") 
       help()


def help():
    print("tcp_client.py [RHOST] [RPORT]")
    sys.exit()
    
def main():
    print("client started...\n")
    GetArgs()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RHOST,RPORT))
    print("connected...\n")
    
    while True:
        message = input("Message:")
        sock.sendall(message.encode("utf-8"))
       
        if "Q" in message:
            break

        message = sock.recv(1024)
        print("Server: %s" % message)
        
    return

if __name__=="__main__":
    main()















    
