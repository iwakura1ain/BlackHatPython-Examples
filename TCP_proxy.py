#!/usr/bin/python3

import sys, socket
import threading

#sys.path.append("/home/dks/Development/Python/GetArgs")
#import GetArgs

LOCALHOST=""
LOCALPORT=0

REMOTEHOST=""
REMOTEPORT=0

RECV_FIRST=False


def ProxyHandler(clnt_sock, remote_host, remote_port, recv_first):
    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_sock.connect((remote_host, remote_port))

    if recv_first:
        remote_buffer = recv_from(remote_sock)
        hexdump(remote_buffer)
        remote_buffer = response_modifyer(remote_buffer)

        if len(remote_buffer):
            print("[<== seding %d bytes to localhost]" % len(remote_buffer))
            clnt_sock.send(remote_buffer)

    while True:
        local_buffer = recv_from(clnt_sock)
        if len(local_buffer):
            print("[==> Received %d bytes from localhost]" % len(local_buffer))
            hexdump(local_buffer)
            local_buffer = request_modifyer(local_buffer)

            remote_sock.send(local_buffer)
            print("[==> Sent to remote]")

        remote_buffer = recv_from(remote_sock)
        if len(remote_buffer):
            print("[<== Received %d bytes from localhost]")
            hexdump(remote_buffer)
            remote_buffer = response_modifyer(remote_buffer)

            clnt_sock.send(remote_buffer)
            print("[<== Sent to localhost]")

        if not len(local_buffer) or not len(remote_buffer):
            print("[Connection broken, quitting...]")
            clnt_sock.close()
            remote_sock.close()
            break
            

def ServLoop(local_host, local_port, remote_host, remote_port, recv_first):
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        serv_sock.bind((local_host, local_port))
        serv_sock.listen(5)
        print("Listening on %s:%d" % (local_host, local_port))
        
    except:
        print("Failed to bind/listen to %s:%d, exiting...." % (local_host, local_port))
        sys.exit(0)

    
    while True:
        clnt_sock, clnt_addr = serv_sock.accept()
        print("Received connection from %s:%d" % (clnt_addr[0], clnt_addr[1]))

        proxy_thread = threading.Thread(target=ProxyHandler,
                                        args=(clnt_sock, remote_host, remote_port, recv_first,))
        
        proxy_thread.start()

#from http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=8):
    result = []
    digits = 4 #if isinstance(src, unicode) else 2
    for i in range(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )

    return b'\n'.join(result)       

def recv_from(connection):
    connection.settimeout(2)
    buffer = ""
    
    try:
        while True:
            data = connection.recv(1024)
            buffer += data

            if not data:
                break
    except:
        pass

    return buffer       

def request_modifyer(buf):
    #modify data sent to remote host
    return buf

def response_modifyer(buf):
    #modify data sent to local host
    return buf

def ParseAddress(addr):
    ip = []
    port = 0
    switch = False

    for ch in addr:
        if ch == ":":
            switch = True
            continue
        elif not switch:
            ip.append(ch)
            continue
        elif switch:
            
            port = 10*port + int(ch)
            continue

    print("IP: %s\nPORT:%d" % ("".join(ip), port))
        
    return "".join(ip), port
    

def Help():
    print("./TCP_proxy.py [localhost]:[localport] [remotehost]:[remoteport] --recv-first")
    sys.exit()

    
def main():
    global LOCALHOST, LOCALPORT, REMOTEHOST, REMOTEPORT, RECV_FIRST
    
    print("TCP proxy from BHP...")

    #args = GetArgs(sys.argv)

    if(sys.argv[1] in ["-h", "--help"]):
        Help()

    if("--recv-first" in sys.argv):
        print("RECV_FIRST: True")
        RECV_FIRST = True
        sys.argv.remove("--recv-first")
        
    LOCALHOST, LOCALPORT = ParseAddress(sys.argv[1])
    REMOTEHOST, REMOTEPORT = ParseAddress(sys.argv[2])

        
    ServLoop(LOCALHOST, LOCALPORT, REMOTEHOST, REMOTEPORT, RECV_FIRST)
 

if __name__=="__main__":
    main()

        















    
