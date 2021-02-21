#!/usr/bin/python3

import threading, queue
import os, time
import requests

THREADS = 20

RHOST = "http://192.168.99.51"
WEBAPP_DIR = "/home/dks/Development/etc/Joomla_3.9.24"
FILTERS = [".jpg", ".png", ".gif", ".css"]
DEPTH = 2
VERBOSE = False

def ParseBlock(path):
    block_list = []
    block = [path[0:6]]

    for ch in path[7:]:
        if(ch == "/"):
            block.append(ch)
            block_list.append("".join(block))
            block = []
            continue
        else:
            block.append(ch)

    return block_list

def Organize(positive_paths):
    organized = []
    prev_len = 0
    prev_path = []

    #print("organizer thread started...")
    while True:
        if(prev_len < len(positive_paths)):
            for path in positive_paths[prev_len+1:]:
                organized.append(ParseBlock(path))
    
            for path in organized[prev_len:]:
                if(DEPTH > len(path)):
                    cur_path = path[:len(path)]
                else:
                    cur_path = path[:DEPTH]

                if(cur_path not in prev_path):   #"".join(cur_path) != "".join(prev_path)):
                    print("200: %s" % "".join(cur_path))
                    prev_path.append(cur_path)

                prev_len += 1
                    
                    
def GenQueue():
    remote_paths = queue.Queue()
    os.chdir(WEBAPP_DIR)

    for dirpath, dirname, filenames in os.walk("."):
        if(dirpath[0] == "."):
            remote_path = dirpath[1:]

        #remote_paths.put(remote_path)
        for filename in filenames:
            if filename[-4:] not in FILTERS:
                remote_paths.put(RHOST + remote_path + "/" + filename)
            
    return remote_paths

def RequestThread(remote_paths, positive_paths):
    #print("request thread started...")    
    while not remote_paths.empty():
        path = str(remote_paths.get())    
        response = requests.get(path)

        if(VERBOSE == True):
            print("%d: %s" % (response.status_code, path))
        else:
            if(response.status_code != 404):
                #print("200: %s" % (path))
                positive_paths.append(path)

        remote_paths.task_done()

    #print("Request thread exited.")
    return

def main():
    print("Joomla scanner from bhp...")

    request_paths = GenQueue()
    positive_paths = []
    request_threads = []
    index = 0

    #print(request_paths.get())

    print("Starting worker threads...")
    for i in range(0,THREADS):
        t = threading.Thread(target=RequestThread, args=(request_paths,positive_paths,))
        request_threads.append(t)
        t.start()

    t = threading.Thread(target=Organize, args=(positive_paths,))
    t.start() 

    for i in range(0,THREADS):
        while True:
            if not request_threads[i].is_alive():
                request_threads[i].join()
                break
            else:
                time.sleep(1)

    print("Scan complete.")    
    return
    
if __name__=="__main__":
    main()



