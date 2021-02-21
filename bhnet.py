#!/usr/bin/python3

import sys, socket
import threading, subprocess

TARGET="0.0.0.0"
PORT=0

LISTEN=False
UPLOAD=False
EXEC=False
SHELL=False

EXEC_COMMAND=""
UPLOAD_DIR=""
VERBOSE=""


'''
def print_opts():
    print("target: %s" % TARGET)
    print("port: %d" % PORT)
  

def GetOpts():
    global HOST, PORT, LISTEN, EXEC, UPLOAD, SHELL, EXEC_COMMAND, UPLOAD_DIR

    if not len(sys.argv[1:]):
        help()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:p:le:su:", ["help","target","port","listen","execute","shell","upload"])

    except getopt.GetoptError as error:
        print(str(error))
        help()

    for o, a in opts:
        if o in ("-h", "--help"):
            help()
        elif o in ("-l", "--listen"):
            LISTEN = True
        elif o in ("-e", "--execute"):
            EXEC = a
        elif o in ("-s", "--shell"):
            SHELL = True
        elif o in ("-u", "--upload"):
            UPLOAD_DIR = a
        elif o in ("-t", "--target"):
            TARGET = a
        elif o in ("-p", "--port"):
            PORT = int(a)
        else:
            assert False, "Unhandled Option"

            
def help():
    exit()


def client_sender(buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((TARGET,PORT))
        if(len(buffer)):
            sock.send(buffer)

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = sock.recv(4096)
                recv_len = len(data)
                respose += data
                
                if recv_len < 4096:
                    break

            print(response)
            
            buffer = input("client received data.")
            buffer += "\n"
            client.send(buffer)

    except:
        print("Error!!")
        sock.close()
        exit()


def client_handler(clnt_sock):
    global UPLOAD
    global EXEC
    global SHELL


    if len(UPLOAD_DIR):
        file_buffer = ""
        while True:
            data = clnt_sock.recv(1024)
            if not data:
                break
            else:
                file_buffer += data

        try:
            fd = open(UPLOAD_DIR, "wb")
            fd.write(file_buffer)
            fd.close()

            clnt_sock.send("Succesfully saved file.")
        except:
            print("Error saving file")

    if EXEC:
        output = run_command(EXEC)
        clnt_sock.send(output)

    if SHELL:
        while True:
            clnt_sock.send("<BHP:#> ")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += clnt_sock.recv(1024)

                response = run_command(cmd_buffer)
                clnt_sock.send(response)
                clnt_sock.send("<BHP:#> ")
    
def server_loop():
    global TARGET
    
    if not len(TARGET):
        TARGET = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TARGET,PORT))
    server.listen(5)

    print("listening on %s:%d" % (TARGET,PORT))
    while True:
        clnt_sock, clnt_addr = server.accept()
        print("recieved connection")

        clnt_thread = threading.Thread(target=client_handler, args=(clnt_sock,))
        clnt_thread.start()


'''

def GetArgs():
    global TARGET, PORT, VERBOSE, LISTEN, EXEC, UPLOAD, SHELL, EXEC_COMMAND, UPLOAD_DIR
    
    offset = 0
    for index in range(1, len(sys.argv)):
        arg = sys.argv[index+offset]
    
        if(arg in ["-h", "--help"]):
            help()

        elif(arg == "-v" or arg == "-vv"):
            VERBOSE=arg[1:]
            print("Verbosity: " + VERBOSE)
            sys.argv.remove(arg)
            offset -= 1

        elif(arg == "--target" or arg == "-t"):
            TARGET = sys.argv[index+offset+1]
            print("TARGET: " + TARGET)
            sys.argv.remove(TARGET)
            sys.argv.remove(arg)
            offset -= 2
            
        elif(arg == "--port" or arg == "-p"):
            PORT = int(sys.argv[index+offset+1])
            print("PORT: " + str(PORT))
            sys.argv.remove(str(PORT))
            sys.argv.remove(arg)
            offset -= 2
      
        elif(arg == "--listen" or arg == "-l"): 
            LISTEN = True
            print("Listen: True")
            sys.argv.remove(arg)
            offset -= 1
            
        elif(arg == "--exec" or arg == "-e"):
            EXEC = True
            print("EXEC: True")
            sys.argv.remove(arg)
            offset -= 1

        elif(arg == "--exec-command"):
            EXEC_COMMAND = sys.argv[index+offset+1]
            print("EXEC_COMMAND: " + EXEC_COMMAND)
            sys.argv.remove(EXEC_COMMAND)
            sys.argv.remove(arg)
            offset -= 2

        elif(arg == "--shell" or arg == "-s"):
            SHELL = True
            print("SHELL: True")
            sys.argv.remove(arg)
            offset -= 1                          


def RunCommand(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except:
        output = "Failed to execute command."

    return output

            
def PrintVerbose(message):
    if( VERBOSE == "v"):
        print(message)


def Connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    sock.connect((TARGET, PORT))
    PrintVerbose("Connected to target")
    
    if SHELL:
        PrintVerbose("Launching dummy shell")
        while True:
            output = b""
            recv_len = 1
            
            while True:
                recv =  sock.recv(1024)
                recv_len = len(recv)
                output += recv

                if recv_len < 1024:
                    break
                    
            print(output.decode("utf-8"))
                
            exec_command = input("")
            print("input: " + exec_command)
            #exec_command += "\n"
            
            sock.send(exec_command.encode("utf-8"))

    elif EXEC:
        PrintVerbose("exec command")
        output = b""
        recv_len = 1

        if(EXEC_COMMAND != ""):
            sock.send(EXEC_COMMAND.encode("utf-8"))
        else:
            PrintVerbose("no exec command")
            exit()
                
        while True:
            recv = sock.recv(1024)
            recv_len = len(recv)
            output += recv
            
            
            if recv_len < 1024:
                break

        print(output.decode("utf-8"))            

    return


def ShellHandler(sock, addr):
    PrintVerbose("spawning dummy shell")

    sock.send("$> ".encode("utf-8"))
    while True:
        recv = b""
        exec_command = b""
        recv_len = 0
        
        while True:
            recv = sock.recv(1024)
            recv_len = len(recv)
            exec_command += recv
            
            if recv_len < 1024:
                break
        
        PrintVerbose("recieved exec: " +  exec_command.decode("utf-8"))
        response = RunCommand(exec_command.decode("utf-8"))
        response += b"$> "

        sock.send(response)

def ExecHandler(sock, addr):
    PrintVerbose("Executing command")

    recv = ""
    while "\n" not in recv.decode("utf-8"):
        recv += sock.recv(1024)
  
    response = RunCommand(recv.decode("utf-8"))
    sock.send(response.encode("utf-8"))


def Listen():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind((TARGET,PORT))
    listen_sock.listen(5)
    PrintVerbose("listening on %s:%d" % (TARGET,PORT))
    
    while True:
        connection_sock, connection_addr = listen_sock.accept()
        PrintVerbose("connection recieved...\n")

        if SHELL:
            connection_thread = threading.Thread(target=ShellHandler,
                                                 args=(connection_sock,connection_addr,))
        elif EXEC:
            connection_thread = threading.Thread(target=ExecHandler,
                                                 args=(connection_sock,connection_addr,))
        
        connection_thread.start()
        
    listen_sock.close()
        

def main():
    print("bhnet.py on BlackHat Python...")
    GetArgs()

    if not LISTEN and len(TARGET) and PORT > 0:
        Connect()
    if LISTEN and PORT > 0:
        Listen()



if __name__=="__main__":
    main()
        



















    
