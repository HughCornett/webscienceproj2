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
			G.add_edge('P'+str(k+1), 'T')

	for startNode in G:
		if startNode[0] == 'n':
			for endNode in G:
				if endNode[0] == 'n' and endNode != startNode:
					G.add_edge(startNode, endNode)

	return G

def pageRank(G, k, B):

	#init the pagerank scores
	pagerank = dict()
	for node in G:
		pagerank[node] = 1.0/len(G)

	#get the number of outgoing edges each node has as a dict
	nodeOutEdges = dict()
	for edge in G.edges():
		if edge[0] not in nodeOutEdges:
			nodeOutEdges[edge[0]] = 0
		nodeOutEdges[edge[0]] += 1

	#if no iterations (or negative number given)
	if k < 1:
		return pagerank

	for i in range(k):
		#init newpagerank with defaults as 0
		newpagerank = dict()
		for node in G:
			newpagerank[node] = 0

		for edge in G.edges():
			if nodeOutEdges[edge[0]] > 0:
				newpagerank[edge[1]] += (pagerank[edge[0]] / nodeOutEdges[edge[0]])
			else:
				newpagerank[edge[0]] += pagerank[edge[0]]

		#scale all node scores by factor of B
		for node in G:
			newpagerank[node] *= B
			newpagerank[node] += float(1-B)/len(G)

		pagerank = newpagerank
		

	return newpagerank

Ts = []
Rs = []
def getLimitT(G):
	lastpagerank = pageRank(G, 0, 0.85)
	lastT = round(lastpagerank['T'], 3)

	lastR = 0
	for i in lastpagerank.keys():
		if i[0] == 'P':
			lastR += lastpagerank[i]
	lastR *= 0.85

	for i in range(1, 100):
		thisT = round(pageRank(G, i, 0.85)['T'], 3)
		if thisT == lastT:
			print("limit T = "+str(lastT)+", R = "+str(lastR)+" (i = "+str(i-1)+")")
			Ts.append(lastT)
			Rs.append(lastR)
			break
		#print("limit T = "+str(thispagerank['T'])+" (i = "+str(i-1)+")")
		lastT = thisT	

for i in range(0, 25):
	G = newGraph(i+1, 5, 1)
	print("f = "+str(i))
	getLimitT(G)
	
G = newGraph(5, 5, 1)

y1 = np.array(Ts)
x1 = np.array(range(0, 25))
plt.scatter(x1, y1)
plt.show()

#draw(G)

