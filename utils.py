import matplotlib.pyplot as plt
import IPython
from IPython.display import SVG
from IPython.display import HTML
from IPython.display import display
import networkx as nx
import StringIO
from networkx.drawing.nx_pydot import read_dot
from networkx.drawing.nx_pydot import from_pydot
from networkx.drawing.nx_agraph import to_agraph
import pydot

'''
Utility Functions
'''
def toGraph(g):
    G = nx.DiGraph()
    for n in g:
        for n2 in g[n]:
            G.add_edge(n,n2)
    return G

def nM(d):
    '''Generate node labeler from dictionary'''
    def m(n, N):
        if n in d:
            N.attr['label'] = n + ' ' + str(d[n])
    return m
def eM(d):
    '''Generate edge labeler from dictionary'''
    def m(e, E):
        if e in d:
            E.attr['label'] = str(d[e])
    return m

def pathColorer(path, color='red'):
    '''Generate edge colorer from path'''
    pairs = set()
    for i in range(len(path)-1):
        l = sorted([path[i], path[i+1]])
        pairs.add((l[0],l[1]))
    def colorer(e,E):
        e = tuple(sorted(e))
        if e in pairs:
            E.attr['color'] = color
    return colorer

def pathNumberer(path):
    '''Generate edge numberer from path'''
    pairs = dict()
    for i in range(len(path)-1):
        l = tuple(sorted([path[i], path[i+1]]))
        pairs[l]=i+1
    def colorer(e,E):
        e = tuple(sorted(e))
        if e in pairs:
            E.attr['label'] = str(pairs[e])
    return colorer

def strongWeakEdges():
    '''Label edges with strength'''
    def labeler(e,E):
        if float(E.attr['weight']) <=0.6:
            E.attr['label'] = "w"
        else:
            E.attr['label'] = "s"
    return labeler

def draw(G, mapping=None, emapping=None):
    '''draw graph with node mapping and emapping'''
    A=to_agraph(G)
    A.graph_attr['overlap']='False'
    if mapping:
        if isinstance(mapping, dict):
            mapping = nM(mapping)
        for n in A.nodes():
            mapping(n, A.get_node(n))
    if emapping:
        if isinstance(emapping, dict):
            emapping = eM(emapping)
        for e in A.edges():
            emapping(e, A.get_edge(e[0],e[1]))
    A.layout()
    output = StringIO.StringIO()
    #A.draw(output, format='svg')
    nx.draw(A, with_labels=True)
    plt.show()

    return SVG(data=output.getvalue())

def fromDot(s):
  P_list = pydot.graph_from_dot_data(s)
  return from_pydot(P_list[0])

def bfs(graph, start):
    '''
    In breadth first search discovered nodes are attached to the end of the queue. Thus,
    the algorithm first searches through all nodes in the same distance from the start node.
    The dictionary visited maps each node to a visiting time and thus keeps track of
    which node was already visited.
    '''
    visited, queue = dict(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited[vertex] = len(visited)
            queue.extend(set(graph[vertex]) - set(visited))
    return visited

def dfs(graph, start):
    '''
    Depth-first-search in graph starting from the node 'start'.
    The algorithm starts at start and explores as far as possible along each branch before backtracking.
    '''
    visited, stack = dict(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited[vertex] = len(visited)
            stack.extend(set(graph[vertex]) - set(visited.keys()))
    return visited

def isStrong(e):
    return float(e['weight']) > 0.5

def neighborPairs(G, a):
    return [ (n1,n2) for n1 in G[a] for n2 in G[a] if n1<n2 ]

def answer(b):
    if b:
        return HTML("<h2 style='color: green;'>Correct</h2>")
    else:
        return HTML("<h2 style='color: red;'>Incorrect</h2>")

def pageRank(G, k, B):

    #init the pagerank scores
    pagerank = dict()
    nodeOutEdges = dict()
    for node in G:
        pagerank[node] = 1.0/len(G)
        nodeOutEdges[node] = 0
    #get the number of outgoing edges each node has as a dict

    for edge in G.edges():

        nodeOutEdges[edge[0]] += 1



    #if no iterations (or negative number given)
    if k < 1:

        return pagerank

    for i in range(k):
        #init newpagerank with defaults as 0
        newpagerank = dict()
        for node in G:
            if nodeOutEdges[node] > 0:
                newpagerank[node] = 0
            else:
                newpagerank[node] = pagerank[node]

        for edge in G.edges():
            newpagerank[edge[1]] += (pagerank[edge[0]] / nodeOutEdges[edge[0]])

        #scale all node scores by factor of B
        for node in G:
            newpagerank[node] *= B
            newpagerank[node] += float(1-B)/len(G)

        pagerank = newpagerank

    return pagerank

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
