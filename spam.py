import networkx as nx
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from graphs import *

def newGraph(f, n, p):
	G = nx.DiGraph()

	for i in range(f):
		G.add_edge('T', 'f'+str(i+1))
		G.add_edge('f'+str(i+1), 'T')

	for j in range(n):
		for k in range(p):
			G.add_edge('n'+str(j+1), 'P'+str(k+1))

	for l in range(p):
		G.add_edge('P'+str(l+1), 'T')

	for startNode in G:
		if startNode[0] == 'n':
			for endNode in G:
				if endNode[0] == 'n' and endNode != startNode:
					G.add_edge(startNode, endNode)

	return G



def getT(G):
	pagerank = nx.pagerank(G, alpha=0.85)

	T = round(pagerank['T'], 3)
	R = 0
	for v in pagerank.keys():
		if v[0] == 'P':
			R += pagerank[v]
	R *= 0.85
	print("limit T = {}, R = {}".format(T,R))

	return T




def experiment(r=50, f=10, n=10, p=10, variable = 'f'):
	Ts = []
	for i in range(0, r):
		if variable == 'f':
			G = newGraph(i+1, n, p)

		elif variable == 'n':
			G = newGraph(f, i+1, p)

		elif variable == 'p':
			G = newGraph(f, n, i+1)

		else:
			print("wrong variable. possible variables: 'f', 'n', 'p'")
			break
		print("{} = {}".format(variable, i))
		Ts.append(getT(G))

	return Ts

y = np.array(experiment(variable='f'))
x = np.array(range(0,50))
plt.subplot(321)
plt.xlabel('number of supporting pages')
plt.ylabel('target\'s PageRank')
plt.scatter(x,y)

y = np.array(experiment(variable='n'))
plt.subplot(322)
plt.xlabel('number of inaccessible pages')
plt.ylabel('target\'s PageRank')
plt.scatter(x,y)

y = np.array(experiment(variable='p'))
plt.subplot(323)
plt.xlabel('number of accessible pages')
plt.ylabel('target\'s PageRank')
plt.scatter(x,y)

plt.show()
