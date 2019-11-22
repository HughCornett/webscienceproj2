import networkx as nx
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from graphs import *
import operator

def newArrowGraph(n):
	G = nx.DiGraph()

	for i in range(1, n):
		G.add_edge(i, i+1)

	return G

def newDirectedGrid(n):
	G = nx.DiGraph()

	if n == 1:
		G.add_node(1)
		return G

	for i in range(0, n):
		for j in range(1, n+1):

			if(j < n):
				G.add_edge((i*n)+j, (i*n)+j+1)
			if(i < n-1):
				G.add_edge((i*n)+j, ((i+1)*n)+j)

	return G

def createlasso():
    G = toGraph({
    'A': ['B', 'E'],
    'B': ['A','C'],
    'C': ['B','D'],
    'D': ['C','E'],
    'E': ['A', 'D','F'],
    'F': ['G']
    })
    return G

def createflower():
    G = toGraph({
    'A': ['B', 'E', 'F'],
    'B': ['A','C', 'G'],
    'C': ['B','D', 'H'],
    'D': ['C','E', 'I'],
    'E': ['A', 'D','J']
    })
    return G

def createInwardStar():
    G = nx.DiGraph()
    for i in range(6):
        G.add_edge(str(i+1), 'A')
    return G

def createSpam(f, n, p):
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

def indegree(G):

	#get the number of incoming edges each node has as a dict
	nodeInEdges = dict()
	for node in G:
		nodeInEdges[node] = 0

	for edge in G.edges():
		nodeInEdges[edge[1]] += 1

	return nodeInEdges

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

def hits(G, k):
    authorities = dict()
    hubs = dict()
    for n in G:
        authorities[n]=1
        hubs[n]=1

    for i in range(k):

        newauthorities = dict()
        newhubs = dict()
        #applying the rule
        for edge in G.edges():
            if edge[1] not in newauthorities:
                newauthorities[edge[1]] = 0
            newauthorities[edge[1]] += hubs[edge[0]]

        #update
        for n in newauthorities.keys():
            authorities[n]=newauthorities[n]

        #applying the rule
        for edge in G.edges():
            if edge[0] not in newhubs:
                newhubs[edge[0]] = 0
            newhubs[edge[0]] += authorities[edge[1]]

        #update
        for n in newhubs.keys():
            hubs[n]=newhubs[n]



    #normalize
    sumauth = sum(authorities.values())
    sumhubs = sum(hubs.values())
    for n in G:
        authorities[n] /= float(sumauth)
        hubs[n] /= float(sumhubs)

    return authorities

def rankDictionary(dictionary):
	return sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

def compareRanking(dic1, dic2):
	distance = 0
	for node1 in range(len(dic1)):
		for node2 in range(len(dic2)):
			if dic1[node1][0] == dic2[node2][0]:
				distance += abs(node2 - node1)
				break
	return distance

def testOnGraph(G):
	hitsrank = hits(G, 100)
	pagerank = pageRank(G, 100, 0.85)
	indegreerank = indegree(G)

	print("HITS: "+str(rankDictionary(hitsrank)))
	print("PageRank: "+str(rankDictionary(pagerank)))
	print("InDegree: "+str(rankDictionary(indegreerank)))

	print("HITS - PageRank: "+str(compareRanking(rankDictionary(hitsrank), rankDictionary(pagerank))))
	print("HITS - InDegree: "+str(compareRanking(rankDictionary(hitsrank), rankDictionary(indegreerank))))
	print("PageRank - InDegree: "+str(compareRanking(rankDictionary(pagerank), rankDictionary(indegreerank))))


print("============")
print("grid graph")
testOnGraph(newDirectedGrid(3))
print("============")
print("arrow graph")
testOnGraph(newArrowGraph(5))
print("============")
print("lasso graph")
testOnGraph(createlasso())
print("============")
print("star graph")
testOnGraph(createInwardStar())
print("============")
print("flower graph")
testOnGraph(createflower())
print("============")
print("spam graph")
testOnGraph(createSpam(3, 3, 1))

G=createSpam(3,3,3)
draw(G)