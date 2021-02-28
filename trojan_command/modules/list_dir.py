#!/usr/bin/python3
import os

def run(**args):
    files = os.listdir(".")
    return str(files)
