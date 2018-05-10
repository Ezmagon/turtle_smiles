#MIT License
#
#Copyright (c) 2018 Matthijs Jonathan Tadema
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

"""
A library containing functions to determine structural features of the molecule
"""

import numpy as np
import networkx as nx
import itertools
import copy

def branches(molecule):
    """
    Parameters:
        molecule, graph representing a molecule
    
    Returns:
        a list of nodes where there are branch points
    """
    degs = np.array(molecule.degree())[:,1]
    branches = []
    ends = []
    for node, deg in enumerate(degs > 2):
        if deg:
            branches.append(node)
    return branches

def backbone(g):
    """
    Parameters:
        g, a molecule graph
    Returns:
        a new graph with the backbone of the molecule
    """
    # Compute minimum spanning tree to remove cycles
    sp = nx.minimum_spanning_tree(g)
    di_g = nx.DiGraph()
    # Convert to directional for longest path
    di_g.add_edges_from(sp.edges())
    path = nx.dag_longest_path(di_g)
    return g.subgraph(path)

def extract_branches(g, n):
    # copy parent graph
    new = nx.Graph(g)
    #  get bb
    bb = backbone(g)
    # Remove all backbone nodes
    to_remove = nx.Graph(bb)
    # Except for the current node
    to_remove.remove_node(n)
    new.remove_nodes_from(to_remove)
    # get only the connected components containing the current node
    # assuming every node can only have one branch
    # but this is not always true
    
    # hold output
    subs = []
    
    # separate into sub graphs
    neighbors = list(new.neighbors(n))
    for ne in neighbors:
        # copy graph
        ne_copy = nx.Graph(new)
        # remove all neighbors except this one
        neighbors_without = copy.deepcopy(neighbors)
        neighbors_without.remove(ne)
        ne_copy.remove_nodes_from(neighbors_without) 
        for s in nx.connected_component_subgraphs(ne_copy):
            if s.has_node(ne):
                subs.append(s)
    # return list of full graphs
    return [ nx.Graph(s) for s in subs ]

def mark_rings(g):
    # find_cycle only finds one ring
    # This doesn't work for molecules with several rings
    ring_edges = nx.find_cycle(g)
    for e in ring_edges:
        g[e[0]][e[1]]["cyclic"] = len(ring_edges)
    return g
