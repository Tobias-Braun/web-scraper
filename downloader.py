#!/usr/bin/env python


import urllib.request as urllib2
from bs4 import *
from urllib.parse  import urljoin
import os
import time
import requests
from pathlib import Path

def strip_url(url: str):
    name = url.split("://")[1]
    name = name.split("?")[0]
    name = name.replace("/", "-")
    assert type(name) == str and len(name) > 0
    return name

def download_page(url, depth=5):
    name = strip_url(url)
    Path(name).mkdir(exist_ok=True)
    urls = crawl([url], depth=depth)
    for u in urls:
        r = requests.get(u)
        with open(os.path.join(name, strip_url(u) + ".html"), 'w+', encoding='utf-8') as file_writer:
            html_str = r.text
            soup = BeautifulSoup(html_str, "html.parser")
            text = soup.get_text().strip()
            file_writer.write(html_str)
        time.sleep(0.05) # sleep 50ms

def crawl(pages, depth=None):
    indexed = set()
    next = set()
    to_index = set(pages) # a list for the main and sub-HTML websites in the main website
    for i in range(depth):
        to_index = to_index - indexed
        for page in to_index:
            try:
                c = urllib2.urlopen(page)
            except:
                print( "Could not open %s" % page)
                continue
            soup = BeautifulSoup(c.read(), "html.parser")
            links = soup('a') #finding all the sub_links
            for link in links:
                if 'href' in dict(link.attrs):
                    link_str = str(link['href']).split("?")[0]
                    if not (link_str.startswith(page) or link_str.startswith("/")):
                        continue
                    url = urljoin(page, link_str)
                    if url.find("'") != -1:
                            continue
                    url = url.split('#')[0] 
                    if url[0:4] == 'http':
                            next.add(url)
            indexed.add(page)
        to_index, next = next, set()
    print(i, indexed)
    return indexed


page = "https://example.org"
download_page(page, depth=2)