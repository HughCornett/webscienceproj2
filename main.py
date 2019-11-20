import networkx as nx
from IPython.display import display
from utils import *
from graphs import *

G = toGraph({
  'A': ['B', 'C'],
  'B': ['C'],
  'D': ['E']
})
draw(G)
#show()