import networkx as nx
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
from utils import *

def newGraph(f, n, p):
	'''
	creates a spam farm with f supporting pages, n inaccessible pages and p accessiblepages
	'''
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




def getTR(G, steps):
	'''
	returns the target's page rank (T) and the external PageRank contribution towards T (R)
	'''
	lastpagerank = pageRank(G, steps, 0.85)

	T = lastpagerank['T']
	R = 0
	for v in lastpagerank.keys():
		if v[0] == 'P':
			R += lastpagerank[v]
	R *= 0.85

	return (T, R)




def experiment(r=50, f=10, n=10, p=10, variable = 'f'):
	'''
	ranks graphs where two out of the f, n and p stays the same and the other one increases from 0 to r
	'''
	Ts = []
	Rs = []
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

		TR = getTR(G, 100)
		Ts.append(TR[0])
		Rs.append(TR[1])
	return (Ts,Rs)

#plotting the results
results = experiment(variable='f')
y = np.array(results[0])
x = np.array(range(0,50))
plt.subplot(321)
plt.title('Figure 1')
plt.xlabel('number of supporting pages')
plt.ylabel('target\'s PageRank')
plt.scatter(x,y)

y = np.array(results[1])
plt.subplot(322)
plt.title('Figure 2')
plt.xlabel('number of supporting pages')
plt.ylabel('sum of accessible pages PageRank (r)')
plt.scatter(x,y)

results = experiment(variable='n')
y = np.array(results[0])
plt.subplot(323)
plt.title('Figure 3')
plt.xlabel('number of inaccessible pages')
plt.ylabel('target\'s PageRank')
plt.scatter(x,y)

y = np.array(results[1])
plt.subplot(324)
plt.title('Figure 4')
plt.xlabel('number of inaccessible pages')
plt.ylabel('sum of accessible pages PageRank (r)')
plt.scatter(x,y)

results = experiment(variable='p')
y = np.array(results[0])
plt.subplot(325)
plt.title('Figure 5')
plt.xlabel('number of accessible pages')
plt.ylabel('target\'s PageRank')
plt.scatter(x,y)

y = np.array(results[1])
plt.subplot(326)
plt.title('Figure 6')
plt.xlabel('number of accessible pages')
plt.ylabel('sum of accessible pages PageRank (r)')
plt.scatter(x,y)

plt.subplots_adjust(hspace = 0.5)

plt.show()
