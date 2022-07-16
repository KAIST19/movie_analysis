import requests
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

URL = 'https://imsdb.com/scripts/Lord-of-the-Rings-Return-of-the-King.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
bolds = soup.find_all("b")
names = set(['GANDALF',
             'BILBO',
             'GALADRIEL',
             'FRODO',
             'SAM',
             'PIPPIN',
             'MERRY',
             'ARWEN',
             'ELROND',
             'LEGOLAS',
             'GIMLI',
             'ARAGORN',
             'DEAGOL',
             'SMEAGOL',
             'GOLLUM',
             'TREEBEARD',
             'EOWYN',
             'THEODEN',
             'DENETHOR',
             'GOTHMOG',
             'ORC',
             'MADRIL',
             'IORLAS',
             'WITCH'
             ])
appears = []

for b in bolds:
    line = b.text.strip().split()
    if 'INT.' in line or 'EXT.' in line:
        appears.append('$')
    else:
        for name in names:
            if name in line:
                appears.append(name)
                break

G = nx.Graph()
G.add_nodes_from(names)

for i in range(len(appears) - 1):
    if appears[i] == '$' or appears[i + 1] == '$':
        continue
    try:
        G.add_edge(appears[i], appears[i + 1], weight=G[appears[i]][appears[i + 1]]['weight'] + 1)
    except:
        G.add_edge(appears[i], appears[i + 1], weight=1)
    
G.remove_edges_from(nx.selfloop_edges(G))

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

for edge in G.edges(data='weight'):
    nx.draw_networkx_edges(G, pos, edgelist=[edge], width=edge[2]/10)
plt.show()