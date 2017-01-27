# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:28:13 2016

@author: z2ro
"""

import graph_tool.all as gt
import numpy as np
import sys, os, os.path
from scipy import linalg
import math
import argparse


def bisect(size,file):
    
    # create random Graph of size N
    #g = gt.random_graph(N,lambda: np.random.poisson(10),directed=False)
    #g = gt.random_graph(N,lambda: (3, 3),directed=False)
    #g = gt.random_graph(100, lambda: (3, 3))
    g = gt.price_network(size,directed=False)
    
    # add Partition Property to graph
    v_partition = g.new_vertex_property('int')
    #g.vertex_properties["partition"] = v_partition
    
    #print(g.list_properties())
    #get the Laplacian
    L = gt.laplacian(g, normalized=False)
    print("Laplacian")
    print(L.todense())
    
    # calculate 2 lowest eigenvector and create Indexvector x
    ew,ev = linalg.eig(L.todense())
    print("eigenvalues")
    print(ew)
    print("eigenvectors")
    print(ev)
    v2 = ev[:,1]
    #print(L.todense())
    #print(v2)
    #v22 = np.sort(v2)
    #print(v22)
    m = np.median(v2)
    #print(m)
    x = [(-1 if i<=m else 1)  for i in v2]
    #print(x) 
    
    for i in range(size):
        v=g.vertex(i)
        v_partition[v] = x[i]
    
    #pos = gt.sfdp_layout(g)
    pos = gt.arf_layout(g, max_iter=0)
    #pos = gt.fruchterman_reingold_layout(g, n_iter=1000)
    #pos = gt.arf_layout(g, max_iter=0)
    gt.graph_draw(g, pos=pos, output="bisection/{0}.png".format(file),vertex_color=[1,1,1,0],vertex_fill_color=v_partition)
    
    
    #state = gt.minimize_nested_blockmodel_dl(g, deg_corr=True)
    #gt.draw_hierarchy(state, output="g3.png")
    #

def getCommandLineArgs():
    parser = argparse.ArgumentParser(description="blabla") 
    parser.add_argument('-n', help='size of the keys in Bits.',required=True,type=int)
    parser.add_argument('-f',help="filename", required=True,type=str)
    args = parser.parse_args()
    return args.n,args.f
        
if __name__ == "__main__":
#    size,file = getCommandLineArgs()
    
    bisect(10,"test")

        