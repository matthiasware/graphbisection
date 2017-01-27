# -*- coding: utf-8 -*-

import graph_tool.all as gt
import numpy as np
from scipy import linalg


def corr(a, b):
    if a == b:
        return 0.999
    else:
        return 0.0001


# output file
file = 'plot.pdf'

# number of nodes
nodes = 1000

# create random Graph of size 'nodes'
g = gt.random_graph(nodes, lambda: np.random.poisson(4), directed=False)

# add Partition Property to graph
v_partition = g.new_vertex_property('int')

# get the Laplacian
L = gt.laplacian(g, normalized=False)

# calculate eval, take evec to lowest and create Indexvector x
# Note: take evec to max eval in order to maximize edges
ew, ev = linalg.eig(L.todense())
seen = {}
unique_eigenvalues = []
for (x, y) in zip(ew, ev):
    if x in seen:
        continue
    seen[x] = 1
    unique_eigenvalues.append((x, y))
v2 = sorted(unique_eigenvalues)[1][1]
m = np.median(v2)
x = [(-1 if i <= m else 1) for i in v2]

for i in range(nodes):
    v = g.vertex(i)
    v_partition[v] = x[i]

pos = gt.arf_layout(g, max_iter=0)
gt.graph_draw(g, pos=pos, output="{0}.pdf".format(file),
              vertex_color=[1, 1, 1, 0],
              vertex_fill_color=v_partition)
