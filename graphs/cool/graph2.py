# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:28:13 2016

@author: z2ro
"""

import graph_tool.all as gt
import numpy as np
from scipy import linalg


def corr(a, b):
    if a == b:
        return 0.999
    else:
        return 0.0001


def bisect(size, file):

    g, bm = gt.random_graph(size, lambda: np.random.poisson(10),
                            model="blockmodel-traditional",
                            directed=False,
                            block_membership=lambda: np.random.randint(10), vertex_corr=corr)

    v_partition = g.new_vertex_property('int')

    L = gt.laplacian(g, normalized=False)

    ew, ev = linalg.eig(L.todense())
    ev = ev.T
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

    for i in range(size):
        v = g.vertex(i)
        v_partition[v] = x[i]

#    pos = gt.arf_layout(g, max_iter=0)
    gt.graph_draw(g, output="bisection/{0}-{1}.pdf".format(file, size), vertex_color=[
                  1, 1, 1, 0], vertex_fill_color=v_partition, edge_color="black")


if __name__ == "__main__":
    bisect(2000, "gt")
