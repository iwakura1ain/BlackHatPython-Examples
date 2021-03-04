import os

def run(args, flags):
    files = os.listdir(".")
    print(files)
    return files
