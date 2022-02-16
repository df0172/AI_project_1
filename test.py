from multiprocessing.dummy import current_process
from nis import cat
from anyio import current_time
import networkx as nx
import matplotlib.pyplot as plt
from numpy import positive
from scipy import rand
from sqlalchemy import null
import random
import time
import logging

from sympy import reduce_abs_inequalities


G = nx.gnp_random_graph(50, .10, seed=1000)





pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='green', )
nx.draw_networkx_labels(G, pos)
#plt.show()

print("---------------")

#for line in range(50):
 #   print(line, "|", nx.degree(G, line))

def rand_loc():
    num = random.randint(0,50)
    return num

# Route optimization.

current = []
new = []



pick = rand_loc()
drop = rand_loc()
while drop == pick:
    drop = rand_loc()
print(nx.shortest_path(G, pick, drop))
current = nx.shortest_path(G,pick, drop)
new = [23, 34, 45, 54]

if not current:
    print("Empty")
else:
    print("not empty")

current = list(set(current + new))

for x in current:
    print(x)









