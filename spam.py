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
			return lastT
		#print("limit T = "+str(thispagerank['T'])+" (i = "+str(i-1)+")")
		lastT = thisT



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
		Ts.append(getLimitT(G))

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
