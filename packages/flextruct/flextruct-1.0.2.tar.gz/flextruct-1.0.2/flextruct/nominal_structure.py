#!/usr/bin/env python2.7
"""
@author: Olga Roudenko
"""

import sys
import os
import logging
import copy
from itertools import compress

from pygraph.algorithms.accessibility import cut_edges

import pygraph_tools


class ChainFragment(object):
    
    def __init__(self, (chain, start_res_nb, end_res_nb)):
        
        self.chain = chain
        self.first_res = start_res_nb
        self.last_res = end_res_nb
        self.len = self.last_res - self.first_res+1
        
        self.start_inx = self.first_res -1
        self.end_inx = self.last_res -1
        
        self.label = '('+ self.chain + str(self.first_res) + ', '+\
            self.chain + str(self.last_res) + ')'


    def shift_indexes(self, first_chain_res):
        
        self.start_inx = self.first_res - first_chain_res 
        self.end_inx = self.last_res - first_chain_res 
        
        
    def __repr__(self):
        
        return self.label
        

class RigidFragment(ChainFragment):

    def __init__(self, chain, start_res_nb, end_res_nb, rb_indx):
        
        ChainFragment.__init__(self, (chain, start_res_nb, end_res_nb))
        
        self.rb_indx = rb_indx


    def __repr__(self):
        
        res = 'RBs[' + str(self.rb_indx) + '] <-'
        res += self.label
        return res


class FlexibleFragment(ChainFragment):

    def __init__(self, chain, start_res_nb, end_res_nb, 
                 from_rb_idx = -1, to_rb_idx = -1):
                     
        ChainFragment.__init__(self, (chain, start_res_nb, end_res_nb))
        
        self.from_rb = from_rb_idx
        self.to_rb = to_rb_idx
        #self.rb_indxs = annex_rb_indxs  # list of length 1 or 2

    def __repr__(self):
        
        res = 'FlexibleFragment '+ self.label
        res +=  ' from RB[' + str(self.from_rb)
        res += '] to RB['+ str(self.to_rb) +']'
        return res


def f7(seq):
    '''
    remove duplicates from a list
    '''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]
    
    
def get_flexible_parts(rigid_bodies_def, chains, log_level = logging.WARNING):
    
    logger = logging.getLogger(str(os.getpid())+':'+__name__+".get_flexible_parts")
    logger.setLevel(log_level)
    
    linkers = []
    terminal_parts = []
    loops = []
    
    rigid_subchains = {}
    for chain_id in chains.keys():
        rigid_fragments = []
        for i  in range(len(rigid_bodies_def)):
            for region in rigid_bodies_def[i]:
                if region[0] == chain_id:
                    rigid_fragments.append(RigidFragment(chain_id, region[1], region[2], i))
        #print rigid_fragments # debug
        #sort them by first_res_nb for ex.
        rigid_fragments.sort(key=lambda s: s.first_res)
        #print rigid_fragments # debug
        rigid_subchains[chain_id] = rigid_fragments

    logger.debug('\nrigid_subchains: '+ str(rigid_subchains))
    
    linkers = []
    terminal_parts = []
    for chain_id in rigid_subchains.keys():
        pieces = rigid_subchains[chain_id]
        if len(pieces) > 1:
            for i in range(len(pieces)-1):  # pieces are supposed sorted !!!
                ff = FlexibleFragment(chain_id, 
                                      pieces[i].last_res+1, 
                                      pieces[i+1].first_res-1, 
                                      pieces[i].rb_indx, 
                                      pieces[i+1].rb_indx)
                if ff.from_rb == ff.to_rb:
                    loops.append(ff)
                else:
                    linkers.append(ff)
                    
        if pieces[0].first_res > chains[chain_id][0]:
            terminal_parts.append(FlexibleFragment(chain_id, 
                                                     chains[chain_id][0], 
                                                     pieces[0].first_res-1, 
                                                     from_rb_idx = -1,
                                                     to_rb_idx = pieces[0].rb_indx))
                                                     
        if pieces[-1].last_res < chains[chain_id][1]:
            terminal_parts.append(FlexibleFragment(chain_id, 
                                                     pieces[-1].last_res+1, 
                                                     chains[chain_id][1],
                                                     from_rb_idx = pieces[-1].rb_indx,
                                                     to_rb_idx = -1))
    
    return linkers, terminal_parts, loops

    
def singlelinker_params(edge, graph):
    params = {}
    
    variable_part = graph.edge_attributes(edge)[0][1] 
    # for double linker we need it to be a vector
    
    #print '\nvariable_part = ' + str(params['variable_part'])
    
    stored_edge = edge
    stored_attrs = graph.edge_attributes(edge)
    stored_label = graph.edge_label(edge)   
    
    graph.del_edge(edge)    
    sub_graphs = pygraph_tools.connected_subgraphs(graph)
    
    '''
    print '\nsub_graphs[0]:'
    print ' nodes =', sub_graphs[0].nodes()
    print ' edges =', sub_graphs[0].edges()
    print '\nsub_graphs[1]:'
    print ' nodes =', sub_graphs[1].nodes()
    print ' edges =', sub_graphs[1].edges()
    '''
    
    # the subgraph from_sg will be fixed 
    # while the subgraph to_sg will be moving
    if variable_part.from_rb in sub_graphs[0].nodes():
        from_sg = sub_graphs[0]
        to_sg = sub_graphs[1]
    else:
        from_sg = sub_graphs[1]
        to_sg = sub_graphs[0]
    
    fixed_part = []
    for n in from_sg.nodes():
        fixed_part += [ChainFragment(a[1]) for a in from_sg.node_attributes(n)]
    phantom_edges = []  # ah pygrah...
    for e in from_sg.edges():
        phantom_edges.append((e[1], e[0]))
        if not e in phantom_edges:
            fixed_part += [ChainFragment((a[1].chain, a[1].first_res, a[1].last_res)) 
                           for a in from_sg.edge_attributes(e)]
    params['fixed_part'] = fixed_part
    
    moving_part = []
    for n in to_sg.nodes():
        moving_part +=[ChainFragment(a[1]) for a in to_sg.node_attributes(n)]
    phantom_edges = []  # ah pygrah...
    for e in to_sg.edges():
        phantom_edges.append((e[1], e[0]))
        if not e in phantom_edges:
            moving_part += [ChainFragment((a[1].chain, a[1].first_res, a[1].last_res)) 
                            for a in to_sg.edge_attributes(e)]
    params['moving_part'] = moving_part
    
    params['variable_part'] = [variable_part]
    #print 'fixed_part = '+ str(params['fixed_part'])
    #print 'moving_part = '+ str(params['moving_part'])
    
    graph.add_edge(stored_edge, label=stored_label, attrs=stored_attrs)    
    
    return params
    
    
def doublelinker_params(edge, graph):
    params = {}
    
    params['variable_part'] = [graph.edge_attributes(edge)[0][1],
                               graph.edge_attributes(edge)[1][1]]
    
    stored_edge = edge
    stored_attrs = graph.edge_attributes(edge)
    stored_label = graph.edge_label(edge)   
    
    graph.del_edge(edge)    
    sub_graphs = pygraph_tools.connected_subgraphs(graph)
    
    params['codirectional'] = False
    # the subgraph from_sg will be fixed 
    # while the subgraph to_sg will be moving
    if params['variable_part'][0].from_rb in sub_graphs[0].nodes():
        from_sg = sub_graphs[0]
        to_sg = sub_graphs[1]
        if params['variable_part'][1].from_rb in sub_graphs[0].nodes():
            params['codirectional'] = True
    else:
        from_sg = sub_graphs[1]
        to_sg = sub_graphs[0]
        if params['variable_part'][1].from_rb in sub_graphs[1].nodes():
            params['codirectional'] = True
            
    fixed_part = []
    for n in from_sg.nodes():
        fixed_part += [ChainFragment(a[1]) for a in from_sg.node_attributes(n)]
    phantom_edges = []  # ah pygrah...
    for e in from_sg.edges():
        phantom_edges.append((e[1], e[0]))
        if not e in phantom_edges:
            fixed_part += [ChainFragment((a[1].chain, a[1].first_res, a[1].last_res)) 
                           for a in from_sg.edge_attributes(e)]
    params['fixed_part'] = fixed_part
    
    moving_part = []
    for n in to_sg.nodes():
        moving_part +=[ChainFragment(a[1]) for a in to_sg.node_attributes(n)]
    phantom_edges = []  # ah pygrah...
    for e in to_sg.edges():
        phantom_edges.append((e[1], e[0]))
        if not e in phantom_edges:
            moving_part += [ChainFragment((a[1].chain, a[1].first_res, a[1].last_res)) 
                            for a in to_sg.edge_attributes(e)]
    params['moving_part'] = moving_part
    '''
    print 'fixed_part = '+ str(params['fixed_part'])
    print 'moving_part = '+ str(params['moving_part'])
    '''
    graph.add_edge(stored_edge, label=stored_label, attrs=stored_attrs)    
    
    return params


def link_variations(linkers, terminal_parts, loops, rigid_bodies_def,
                    log_level = logging.WARNING): 
    '''
    '''    
    logger = logging.getLogger(str(os.getpid())+':'+__name__+".link_variations")
    logger.setLevel(log_level)
    
    everything_but_linkers =  copy.deepcopy(rigid_bodies_def)
    for l in loops:
        everything_but_linkers[l.from_rb].append((l.chain, l.first_res, l.last_res))
    for t in terminal_parts:
        if t.from_rb == -1:
            everything_but_linkers[t.to_rb].append((t.chain, t.first_res, t.last_res))
        else:
            everything_but_linkers[t.from_rb].append((t.chain, t.first_res, t.last_res))        

    logger.debug('  everything_but_linkers =\n\t'+ str(everything_but_linkers)+'\n')    
    
    
    g = pygraph_tools.build_graph(linkers, everything_but_linkers, log_level) 
    logger.debug(' edges = '+ str(g.edges()))       
    #print g.edges()  # DEBUG      
    """
    dot = write(g)
    gvv = gv.readstring(dot)
    gv.layout(gvv,'dot')
    #gv.render(gvv,'png','rb1_ir3.png')
    gv.render(gvv,'png', png_path)
    """    
    
    variations = {}
    
    cutedges = cut_edges(g)
    logger.debug(' cutedges = ' + str(cutedges))
    for e in cutedges:
        if g.edge_weight(e) == 1:
            logger.debug(" cut edge: "+ str(e))
            variations[g.edge_label(e)] = {'type': 'SingleLinker',
                                           'rating': 1,  # default rating
                                           'params': singlelinker_params(e, g)}
        else:
            variations[g.edge_label(e)] = {'type': 'DoubleLinker', 
                                           'rating': 1, # default rating    
                                           'params': doublelinker_params(e, g)}
    #print '\nvariations I = ', str(variations)                                       
                                           
    for  e in cutedges:                                
        g.del_edge(e)
    
    sub_graphs = pygraph_tools.connected_subgraphs(g)
                            
    for sg in sub_graphs:
        #print sg.edges()  # DEBUG
        #single_edges = [e for e in sg.edges and sg.edge_weight(e)==1]
        seen_edges = []
        #for se in single_edges and not se in seen_edges:
        for se in sg.edges(): 
            if sg.edge_weight(se)==1 and not se in seen_edges:
                #print '\nremoving ' + str(se)  # DEBUG
                stored_edge = se
                stored_attrs = sg.edge_attributes(se)
                stored_label = sg.edge_label(se)
                
                seen_edges += [se, (se[1], se[0])] # ah pygrah...
                
                sg.del_edge(se)
                curr_cutedges = cut_edges(sg)
                #print 'cut edges: ' + str(curr_cutedges)  # DEBUG
                #print 'seen_edges = ' + str(seen_edges)  # DEBUG
                
                counted_ones = []
                for e in curr_cutedges:
                    counted_ones.append((e[1], e[0])) # ah pygrah...
                    #print 'counted_ones = ' + str(counted_ones)  # DEBUG
                    
                    if (sg.edge_weight(e) == 1 and 
                        not e in seen_edges and not e in counted_ones):
                            
                        #print 'chosen edge ' + str(e)
                        label = stored_label + ', ' + sg.edge_label(e)
                        variations[label] = {'type': 'DoubleLinker', 
                                             'rating': 1, # default rating
                                             'params': doublelinker_params(e, g)}
                        
                sg.add_edge(stored_edge, label=stored_label, attrs=stored_attrs)
    #print '\nvariations = ' + str(variations)
    return variations
    
    
def terminal_variations(terminal_parts, linkers, loops, rigid_bodies_def,
                        log_level = logging.WARNING):
    
    logger = logging.getLogger(str(os.getpid())+':'+__name__+".terminal_variations")
    logger.setLevel(log_level)
    
    variations = {}  
    rigid_fragments = []
    for i in range(len(rigid_bodies_def)):
        rb_def_i = rigid_bodies_def[i]
        for j in range(len(rb_def_i)):
            rigid_fragments.append(RigidFragment(rb_def_i[j][0], # chain
                                                 rb_def_i[j][1], # first_res
                                                 rb_def_i[j][2], # last_res
                                                 i))     
    all_except_terminal_parts =  rigid_fragments + linkers + loops
    
    for i in range(len(terminal_parts)):
        curr_fragment = terminal_parts[i]
        
        mask = [1]*len(terminal_parts)
        mask[i]=0
        all_except_curr_fragment =  all_except_terminal_parts + list(compress(terminal_parts, mask))
            
        struct_parts = {}
        struct_parts['variable_part'] = [curr_fragment]
        # it is a list because of the double linkers
        struct_parts['fixed_part'] = []
        struct_parts['moving_part'] = []
        
        if curr_fragment.from_rb == -1:
            struct_parts['moving_part'] = all_except_curr_fragment
        elif  curr_fragment.to_rb == -1:
            struct_parts['fixed_part'] = all_except_curr_fragment
        else:
            logger.error(' Invalid argument')
        
        variations[curr_fragment.label] = {'type': 'SingleLinker',
                                           'rating': 1,  # default rating
                                           'params': struct_parts}
    return variations
    
"""
# finally did not need this function
#
def loop_variations(terminal_parts, linkers, loops, rigid_bodies_def,
                        log_level = logging.WARNING):
    
    logger = logging.getLogger(str(os.getpid())+':'+__name__+".loop_variations")
    logger.setLevel(log_level)
    
    variations = {}  
    rigid_fragments = []
    for i in range(len(rigid_bodies_def)):
        rb_def_i = rigid_bodies_def[i]
        for j in range(len(rb_def_i)):
            rigid_fragments.append(RigidFragment(rb_def_i[j][0], # chain
                                                 rb_def_i[j][1], # first_res
                                                 rb_def_i[j][2], # last_res
                                                 i))     
    all_except_loops =  rigid_fragments + linkers + terminal_parts
    
    for i in range(len(loops)):
        curr_fragment = loops[i]
        
        mask = [1]*len(loops)
        mask[i]=0
        all_except_curr_fragment =  all_except_loops + list(compress(loops, mask))
            
        
        params = {}
        params['codirectional'] = False  # a loop transformed into a double linker
        params['fixed_part'] = all_except_curr_fragment
        
        # rigid body has to be added here
        
        
        params['moving_part'] = []
        
        params['variable_part'] = [curr_fragment]
        
    
        variations[curr_fragment.label] = {'type': 'DoubleLinker',
                                           'rating': 1,  # default rating
                                           'params': params}
    return variations    
""" 
    
    
    
def get_chains(pdb_path):
    
    chains = {}
    all_lines = open(pdb_path, "r").readlines()
    
    #atom_lines = [l for l in all_lines if l[:6] == "ATOM  " or l[:6] == "TER   "]
    atom_lines = [l for l in all_lines if l[:6] == "ATOM  "]
    chain_names = f7([l[21] for l in atom_lines])
    for ch in chain_names:
        ch_lines = [l for l in atom_lines if l[21] == ch]
        chains[ch] = (int(ch_lines[0][22:26]), int(ch_lines[-1][22:26]))

    hetatm_lines = [l for l in all_lines if l[:6] == "HETATM"]
    hetatm_names = f7([l[17:20].strip() for l in hetatm_lines])
    #print hetatm_names
    '''
    for ha in hetatm_names:
        ha_lines = [l for l in hetatm_lines if l[17:20].strip() == ha]        
        chains[ha] = (int(ha_lines[0][22:26]), int(ha_lines[-1][22:26]))
    '''
    return chains, hetatm_names
    

def get_variations(rigid_bodies_def, pdb_path, flex_minlens, log_level = logging.WARNING):
    '''
    flex_minlens = {'single' : 3, 'term' : 3, 'double' : 6, 'loop' : 13}
    '''
    
    logger = logging.getLogger(str(os.getpid())+':'+__name__+".get_variations")
    logger.setLevel(log_level)
    
    logger.debug('  rigid bodies =\n\t'+ str(rigid_bodies_def)+'\n')
        
    #chains = utils_mmtk.auto_region_def(pdb_path)
    chains, ligands = get_chains(pdb_path)
    logger.debug('  chains =\n\t'+ str(chains)+'\n')
    logger.debug('  ligands =\n\t'+ str(ligands)+'\n')
    # TODO: test the coherence between the chains read from the pdb file 
    # and the rigid bodies read from the config file
    for rb in rigid_bodies_def:
        if any([not rb_i[0] in chains.keys()+ligands for rb_i in rb]):
            msg = ' Invalid rigid bodies config: incoherence with pdb structure'
            logger.error(msg)
            raise Exception(msg)
            
    linkers, terminal_parts, loops = get_flexible_parts(rigid_bodies_def, chains,
                                                        log_level)
    
    logger.debug('  linkers =\n\t'+str( linkers)+'\n')
    logger.debug('  terminal_parts =\n\t'+ str(terminal_parts)+'\n')
    logger.debug('  loops =\n\t'+ str(loops)+'\n') 
    
    logger.info(' ' + str(len(linkers)) + ' linkers, ' +
                str(len(terminal_parts))+ ' terminal parts and ' +
                str(len(loops)) + ' loops are detected\n')
                
    # -----------------------------------------------
    logger.debug(' Transforming loops into linkers')
    # -----------------------------------------------
    for l in loops:
        if l.len >= flex_minlens['loop']:
            #print l.len
            middle_res = l.first_res+(l.last_res-l.first_res)/2
            rigid_bodies_def.append([(l.chain, middle_res, middle_res)])
        
        else:
            msg = 'Too short loop:  '+ str(l)
            msg += '\nPlease choose between allongating it up to at least '+str(flex_minlens['loop'])+ ' residues and ignoring it'
            logger.error(msg)
            raise Exception(msg)
            # join all l's resudues to l.from_rb
        
    linkers, terminal_parts, loops = get_flexible_parts(rigid_bodies_def, chains,
                                                        log_level)
    
    logger.debug('  linkers =\n\t'+str( linkers)+'\n')
    logger.debug('  terminal_parts =\n\t'+ str(terminal_parts)+'\n')
    logger.debug('  loops =\n\t'+ str(loops)+'\n')
    
    
    logger.info(' ' + str(len(linkers)) + ' linkers, ' +
                str(len(terminal_parts))+ ' terminal parts and ' +
                str(len(loops)) + ' loops are detected\n')
    # ----------------------------------------------------------------------
    
    variations = link_variations(linkers, terminal_parts, loops, rigid_bodies_def,
                                 log_level)
                                 
                                 
    for label in variations.keys():
        
        #print variations[label]['params']['variable_part']
        
        if (variations[label]['type'] == 'DoubleLinker' and 
            (variations[label]['params']['variable_part'][0].len < flex_minlens['double'] or
             variations[label]['params']['variable_part'][1].len < flex_minlens['double'])
             
            or variations[label]['type'] == 'SingleLinker' and 
            variations[label]['params']['variable_part'][0].len < flex_minlens['single']):
                
                sys.tracebacklimit = -1
                raise Exception(' Too short variable part: '+ label)
                                
        variations[label]['rating'] = 2*max([ fragment.len for fragment in variations[label]['params']['variable_part'] ])        
        
    term_variations = terminal_variations(terminal_parts, linkers, loops, 
                                          rigid_bodies_def,
                                          log_level)
    for label in term_variations.keys():
        term_variations[label]['rating'] = term_variations[label]['params']['variable_part'][0].len
        #print term_variations[label]['params']['fixed_part']  # DEBUG
        #print term_variations[label]['params']['moving_part']  # DEBUG
    variations.update(term_variations)
    
    logger.debug(' variations:\n'+ str(variations))
    
    # TODO comment
    for label in variations.keys():
        for f in (variations[label]['params']['variable_part']+
                  variations[label]['params']['fixed_part']+
                  variations[label]['params']['moving_part']):
            if f.chain in chains.keys():
                f.shift_indexes(chains[f.chain][0])
            elif f.chain in ligands:
                f.shift_indexes(f.first_res)
#            print f
#            print f.start_inx
#            print f.end_inx
#    sys.exit()
    return variations


if __name__ == "__main__":
    
    pdb_path =  '/home/roudenko/work/swing/saxs/data/PtPn4/PTPN4_PDZ_PTP_ext_helix_min_1.pdb'
    rb1 = [('A', 512, 602)]
    rb2 = [('A', 607, 617)]
    rb3 = [('A', 639, 913)]
    rigid_bodies_def = [rb2, rb1, rb3]
    png_path =  '/home/roudenko/work/swing/saxs/data/PtPn4/ptpn4.png'
    
    '''
    pdb_path =  '/home/roudenko/work/swing/saxs/data/RB1_IR3/compare/RB1_IR3_5.pdb'
    rb1 = [('X', 1, 33), ('Y', 1, 33), ('B', 122, 210), ('C', 122, 219), ('ZN1', 812, 812), ('ZN2', 813, 813), ('ZN3', 812, 812), ('ZN4', 813, 813)]
    rb2 = [('B', 236, 458), ('C', 236, 458)]
    rigid_bodies_def = [rb2, rb1]
    png_path =  '/home/roudenko/work/swing/saxs/data/RB1_IR3/compare/rb1_ir3.png'
    '''
        
    print get_variations(rigid_bodies_def, pdb_path)
        