#!/usr/bin/env python2.7
"""
@author: Olga Roudenko
"""

import sys
import os
import numpy
import logging

from pygraph.classes.graph import graph
from pygraph.algorithms.accessibility import *
from pygraph.readwrite.dot import write
#import gv


def connected_subgraphs(g):
    
    nodes_ccomps = connected_components(g)  # from pygraph.algorithms.accessibility
    #print 'connected_components: ' + str(nodes_ccomps)  # DEBUG
    # [v for v in nodes_ccomps.itervalues()]
    
    ccomps_nodes = {ccomps:nodes for nodes, ccomps in nodes_ccomps.items()}    
    sub_graphs = [graph() for i in range(len(ccomps_nodes.keys()))]
    
    for n, cc in nodes_ccomps.items(): 
        sub_graphs[cc-1].add_node(n, attrs = g.node_attributes(n))
#    for sg in sub_graphs:
#        print sg.nodes()     
    # print g.edges()  # DEBUG
    
    for n, cc in nodes_ccomps.items(): 
        sg = sub_graphs[cc-1]
        for e in g.edges():
            if (e[0] == n or e[1] == n) and not sg.has_edge(e):
                sg.add_edge(e, wt = g.edge_weight(e), 
                            label = g.edge_label(e),
                            attrs = g.edge_attributes(e))
    return sub_graphs
    
    
def build_graph(linkers, rigid_bodies_def, log_level = logging.WARNING):
    
    logger = logging.getLogger(str(os.getpid())+':'+__name__+".build_graph")
    logger.setLevel(log_level)
    
    gr = graph()
    gr.add_nodes(numpy.arange(len(rigid_bodies_def)))
    
    for node in gr.nodes():
        for i in range(len(rigid_bodies_def[node])):
            gr.add_node_attribute(node, (i, rigid_bodies_def[node][i]))
        logger.debug(" Node " + str(node) + " attrs =  " + str(gr.node_attributes(node)))
    
    for l in linkers:
        ledge = (l.from_rb, l.to_rb)
        if not gr.has_edge(ledge):
            gr.add_edge(ledge)
            gr.add_edge_attribute(ledge, (1, l))
            gr.set_edge_weight(ledge, 1)
            gr.set_edge_label(ledge, l.label)
        elif gr.edge_weight(ledge) == 1:
            gr.add_edge_attribute(ledge, (2, l))
            gr.set_edge_weight(ledge, 2)
            gr.set_edge_label(ledge, gr.edge_label(ledge)+', '+l.label)
        else:
            print "Dadimodo cannot work with such a topology"
            sys.exit()
        logger.debug(" Edge " + str(ledge) + " attrs = " + str(gr.edge_attributes(ledge)))
        
    return gr



if __name__ == "__main__":

    chains = utils_mmtk.auto_region_def(pdb_path)
    print '\nchains:', chains

    g = rigidbodies2graph(chains, rigid_bodies_def)

    #print 'cycles: ' + str(graph_utils.find_all_cycles(g))
    print 'connected_components: ' + str(connected_components(g))
    print 'accessibility: ' + str(accessibility(g))
    
    dot = write(g)
    gvv = gv.readstring(dot)
    gv.layout(gvv,'dot')
    #gv.render(gvv,'png','rb1_ir3.png')
    gv.render(gvv,'png', png_path)

