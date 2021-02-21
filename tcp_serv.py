#!/usr/bin/python3

import socket
import threading
import sys
import os

LHOST="0.0.0.0"
LPORT=None


def GetArg():
    global LPORT

    offset = 0
    for index in range(1, len(sys.argv)):
        arg = sys.argv[index+offset]
    
        if(arg == "-h" or arg == "--help"):
            help()

        elif(arg == "-v" or arg == "-vv"):
            sys.argv.remove(arg)
            offset -= 1
            help()

    if(len(sys.argv) == 2):
        LPORT = int(sys.argv[1])
        
    else:
       print("!!Argument Error!!") 
       help()


def help():
    print("tcp_serv.py [LPORT]")
    sys.exit()

def client_handler(clnt_sock):    
    while True:
        message = clnt_sock.recv(1024)
        print("client: %s\n" % message)
        clnt_sock.sendall("message recieved!".encode("utf-8"))

        if "Q" in str(message):
            break
        
    clnt_sock.close()
    print("client disconncted")
    
    return
    
def main():
    clnt_threads = []
    
    print("serv started...\n")
    GetArg()
    
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind((LHOST,LPORT))
    serv_sock.listen(3)
    print("listening on %s:%d" % (LHOST,LPORT))

    while True:
        clnt_sock, addr = serv_sock.accept()
        print("client connected\n")
    
        clnt_thread = threading.Thread(target=client_handler, args=(clnt_sock,))
        clnt_threads.append(clnt_thread)
        clnt_thread.start()


    for thread in clnt_threads:
        thread.join()
        
    return

if __name__=="__main__":
    main()















    
