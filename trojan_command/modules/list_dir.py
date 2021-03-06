import os

def run(args, flags):
    files = os.listdir(".")
    print(str(files))
    return str(files)
