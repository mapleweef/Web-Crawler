#!/usr/bin/python2
from bs4 import BeautifulSoup
import urllib2 as urllib
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
import urlparse


def check_link(url):
    filetype = urlparse.urlparse(url).path.split('/')[-1:][0].split('.')[-1:][0]

    if  (filetype != 'jpg' and filetype != 'pdf' and filetype != 'jpeg'):#checks to make sure link is not a file
        return True
    else:
        return False

    

root=('http://businessandit.uoit.ca')
processing = Queue()
processed = []
count = 0
graph = nx.DiGraph()
graph.add_node(root)
processing.push(root)


while not processing.is_empty():
    current = processing.pop()

    try:
        html_page = urllib.urlopen(current, timeout = 90)
    except:
        #print('Error downloading %s' %current) throws error saying it cant desplay string
        continue

    try:
        soup = BeautifulSoup(html_page, "html.parser")
    except:
        continue

    for link in soup.findAll('a'):
        url = link.get('href')
        if url and check_link(url):
            if 'http' in url and 'uoit.ca' in url:
                graph.add_edge(current, url)
                if url not in processed and url not in processing:
                    processing.push(url)
                    processed.append(url)
                
    count += 1
    if count % 500 == 0:
        nx.write_gexf(graph, "test.gexf")


nx.write_gexf(graph,"test.gexf")
