#!/usr/bin/python3

import urllib3
#import csv
from bs4 import BeautifulSoup

url = "http://localhost/index.html"
http = urllib3.PoolManager()

response = http.request("GET", url)
soup = BeautifulSoup(response.data, features="lxml")

lines = soup.li
lines.decompose()


