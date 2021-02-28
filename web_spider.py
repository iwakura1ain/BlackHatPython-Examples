#!/usr/bin/python3

#import urllib3
#import csv
import requests
from bs4 import BeautifulSoup

URL = "http://127.0.0.1/dirtest.html"
DEPTH = 5


#TODO: Use functions instead of in init for link walking, otherwise it's a pain to thread!
#TODO: Found links loop bak into themselves...

class UrlNode:  
    def __init__(self, parent, url):
        self.parent = parent
        self.urls = self.GetChildUrls(url)
        self.children = []

    def GetChildUrls(self, url):
        urls = [url]       

        response = requests.get(urls[0])
        soup = BeautifulSoup(response.text, features="lxml")

        for found in soup.find_all("a"):
            found_url = found.get("href")
            if found_url is None:
                break

            if(found_url == "" or found_url[0] in ("+", "?", "#")):
                continue
            elif(found_url[0:4] == "http"):
                print("found domain: " + found_url)
                urls.append(found_url)
            elif(found_url[0:1] == "/"):
                if(found_url[0:2] == "//"):
                    print("found subdom: " + "http:" + found_url)
                    urls.append("http:" + found_url)
                else:
                    #TODO: append to site root instead of parent, otherwise links keep looping back into themselves
                    print("found subdir: " + urls[0] + found_url) 
                    urls.append(urls[0] + found_url)
            
        return urls
    
    def ParseUrl(self, url):
        print(url)
        start = str(url).index('http')
        end = str(url).index('">')

        return str(url)[start:end]

def GenTree(parent, depth):
    if(len(parent.urls) > 1 and depth <= DEPTH):
        for url in parent.urls[1:]:
            parent.children.append(UrlNode(parent,url))
        for child in parent.children:
            GenTree(child, depth+1)
            
    return

def WalkTree(node, indent):
    print("%s ->: %s " % (indent, node.urls[0]))

    child_count = len(node.children)
    if(child_count == 0):
        return
    else:
        for i in range(0,child_count):
            WalkTree(node.children[i], indent + "  ")

    return
    
def main():
    print("web scrapper started...")
    
    first_node = UrlNode(None,URL)
    GenTree(first_node, 0)

    WalkTree(first_node, "")
    

if __name__=="__main__":
    main()
    





