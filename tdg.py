import networkx as nx
import random
import numpy as np
from scipy.optimize import curve_fit
import math
import matplotlib.pyplot as plt

def edge_remove(x,y,n):
    """Computes the result of the (x, y) edge-remove process on n vertices.
    
    For every ordered pair of positive integers (x, y) and integer n >= max(x, y), 
    computes the directed graph on which the (x, y) edge-remove process terminates.
    Args:
        x,y,n: positive integers.
    Returns:
        A networkx DiGraph.
    """
    G = nx.DiGraph()
    possible_edge = set()
    for i in range(n):
        G.add_node(i)
        for j in range(i+1, n):
            G.add_edge(i, j)
            possible_edge.add((i,j))
    counter = 0
    while 0 == 0:
        edge_list = list(possible_edge)
        if len(edge_list) == 0:
            return G
        k = random.randrange(len(edge_list))
        edge_cand = edge_list[k]
        candG = G.copy()
        candG.remove_edge(edge_cand[0], edge_cand[1])
        cand_exterior = exterior_vertices(candG)
        if len(cand_exterior[0]) <= x and len(cand_exterior[1]) <= y:
            G = candG.copy()
        possible_edge.remove((edge_cand[0],edge_cand[1]))

def edge_add(x,y,n):
    """Computes the result of the (x, y) edge-add process on n vertices.
    
    For every ordered pair of positive integers (x, y) and integer n >= max(x, y), 
    computes the directed graph on which the (x, y) edge-add process terminates.
    Args:
        x,y,n: positive integers.
    Returns:
        A networkx DiGraph.
    """
    G = nx.DiGraph()
    possible_edge = set()
    for i in range(n):
        G.add_node(i)
        for j in range(i+1, n):
            possible_edge.add((i, j))
    while 0 == 0:
        edge_list = list(possible_edge)
        if len(edge_list) == 0:
            return G
        k = random.randrange(len(edge_list))
        edge_cand = edge_list[k]
        candG = G.copy()
        candG.add_edge(edge_cand[0], edge_cand[1])
        cand_exterior = exterior_vertices(candG)
        if len(cand_exterior[0]) >= x and len(cand_exterior[1]) >= y:
            G = candG.copy()
        if len(cand_exterior[0]) == x and len(cand_exterior[1]) == y:
            return G
        possible_edge.remove((edge_cand[0],edge_cand[1]))            

def xy_check(G,x,y):
    """Checks whether G is an (x, y) task-dependency graph.
    
    For any directed acyclic graph G, returns 1 if G has x initial vertices and y terminal
    vertices, and returns 0 otherwise.
    Args:
        G: a networkx DiGraph.
        x, y: positive integers.
    Returns:
        1 or 0, depending on whether or not G has x initial vertices and y terminal vertices.
    """
    exterior = exterior_vertices(G)
    if len(exterior[0]) == x and len(exterior[1]) == y:
        return 1
    else:
        return 0
        
def exterior_vertices(G):
    """Computes the lists of initial and terminal vertices in a directed acyclic graph G.
    
    For any directed acyclic graph G, computes two lists: initial vertices which have no 
    incoming edges, and terminal vertices which have no outgoing edges.
    Args:
        G: a networkx DiGraph.
    Returns:
        a list of two lists, one with initial vertices and the other with terminal vertices.
    """
    initial = []
    terminal = []
    node_list = list(G)
    for i in node_list:
        if G.in_degree(i) == 0:
            initial.append(i)
        if G.out_degree(i) == 0:
            terminal.append(i)
    return [initial, terminal]

def prob_xy(max_order,x,y, trials, k):
    """Computes a string of ratios of number of (x,y) task-dependency graphs over number
    of task-dependency graphs generated by the (x,y) edge-remove process when k = 0 and 
    (x,y) edge-add process when k = 1 on n vertices for n = 5 to max_order.
    
    For any integer max_order >= 5, positive integers x,y,trials, and k in {0,1}:
    outputs a string of ratios of number of (x,y) task-dependency graphs over number
    of task-dependency graphs generated by the (x,y) edge-remove process when k = 0 
    and (x,y) edge-add process when k = 1 on n vertices for n = 5 to max_order, where
    consecutive ratios are separated by '&'s and the output ends with '\\\'
    Args:
        max_order: integer >= 5
        x, y, trials: positive integers
        k: 0 or 1
    Returns:
        a string of ratios
    """
    row_of_prob = '('+str(x)+', '+str(y)+')'
    for order in range(5, max_order+1):
        xy_arr = []
        for m in range(trials):
            if k == 0:
                min_tdg = edge_remove(x,y,order)
            elif k == 1:
                min_tdg = edge_add(x,y,order)
            xy_arr.append(xy_check(min_tdg,x,y))
        row_of_prob = row_of_prob + ' & '+str(np.mean(np.array(xy_arr)))
    row_of_prob = row_of_prob + ' \\\ '
    return row_of_prob

def line_fit(x,a,b):
    return a * x + b

def quad_fit(x,a,b,c):
    return a * x**2 + b * x + c

def lin_over_log_fit(x,a,b):
    return a * float(x)/math.log(float(x)) + b

def lin_ol_fit(x_vect, a, b):
    return [lin_over_log_fit(x,a,b) for x in x_vect]

def sqrt_fit(x_vect,a,b):
    return [a * math.sqrt(x) + b for x in x_vect]

def log_fit(x_vect,a,b,c):
    return [a * math.log(x+b) + c for x in x_vect]

def table_edge_cpl(max_order):
    figure, axis = plt.subplots(2, 2)
    for k in [0,1]:
        x = []
        y_edge = []
        y_cpl = []
        
        for order in range(3, max_order):
            edge_count_arr = []
            cpl_count_arr = []
            for m in range(1000):
                if k == 0:
                    min_tdg = edge_remove(1,1,order)
                elif k == 1:
                    min_tdg = edge_add(1,1,order)
                ecount = min_tdg.number_of_edges()
                cpl = nx.dag_longest_path_length(min_tdg)
                edge_count_arr.append(ecount)
                cpl_count_arr.append(cpl)
            print(order, np.mean(np.array(edge_count_arr)), np.mean(np.array(cpl_count_arr)))
            x.append(order)
            y_edge.append(np.mean(np.array(edge_count_arr)))
            y_cpl.append(np.mean(np.array(cpl_count_arr)))
        x_np = np.array(x)
        y_edge_np = np.array(y_edge)
        y_cpl_np = np.array(y_cpl)
        if k == 0:
            edge_fit, ef_pcov = curve_fit(line_fit, x_np, y_edge_np)
            cpl_fit, cf_pcov = curve_fit(line_fit, x_np, y_cpl_np)
            alt_cpl_fit, acf_pcov = curve_fit(lin_ol_fit, x_np, y_cpl_np)
            sq_cpl_fit, scf_pcov = curve_fit(sqrt_fit, x_np, y_cpl_np)
            log_cpl_fit, lcf_pcov = curve_fit(log_fit, x_np, y_cpl_np)
            x_new = np.linspace(2,max_order)
           
            axis[0, 0].plot(x_np, y_edge_np, 'o', label='data points')
            axis[0, 0].plot(x_new, line_fit(x_new, *edge_fit), '-', label='fit curve '+str(round(edge_fit[0],3))+'x'+str(round(edge_fit[1],3)))
            axis[0, 0].axis([2, max_order, 0, y_edge[-1]*1.2])
            axis[0, 0].set_title("(a)")
            print('(a) fit curve '+str(round(edge_fit[0],3))+'x'+str(round(edge_fit[1],3)))
            
            axis[0, 1].plot(x_np, y_cpl_np, 'o', label='data points')
            axis[0, 1].plot(x_new, log_fit(x_new, *log_cpl_fit), '-', label='fit curve '+str(round(log_cpl_fit[0],3))+'log(x+'+str(round(log_cpl_fit[1],3))+')'+str(round(log_cpl_fit[2],3)))
            axis[0, 1].axis([2, max_order, 0, y_cpl[-1]*1.2])
            axis[0, 1].set_title("(b)")
            print('(b) fit curve '+str(round(log_cpl_fit[0],3))+'log(x+'+str(round(log_cpl_fit[1],3))+')'+str(round(log_cpl_fit[2],3)))
            
        elif k == 1:
            edge_fit, ef_pcov = curve_fit(quad_fit, x_np, y_edge_np)
            cpl_fit, cf_pcov = curve_fit(line_fit, x_np, y_cpl_np)
            
            x_new = np.linspace(2,max_order)
            axis[1,0].plot(x_np, y_edge_np, 'o', label='data points')
            axis[1,0].plot(x_new, quad_fit(x_new, *edge_fit), '-', label='fit curve '+str(round(edge_fit[0],3))+'x^2'+str(round(edge_fit[1],3))+'x+'+str(round(edge_fit[2],3)))
            axis[1,0].axis([2, max_order, 0, y_edge[-1]*1.2])
            axis[1,0].set_title("(c)")
            print('(c) fit curve '+str(round(edge_fit[0],3))+'x^2'+str(round(edge_fit[1],3))+'x+'+str(round(edge_fit[2],3)))
            
            axis[1,1].plot(x_np, y_cpl_np, 'o', label='data points')
            axis[1,1].plot(x_new, line_fit(x_new, *cpl_fit), '-', label='fit curve '+str(round(cpl_fit[0],3))+'x'+str(round(cpl_fit[1],3)))
            axis[1,1].axis([2, max_order, 0, y_cpl[-1]*1.2])
            axis[1, 1].set_title("(d)")
            print('(d) fit curve '+str(round(cpl_fit[0],3))+'x'+str(round(cpl_fit[1],3)))
            
            plt.show()

    return


print(prob_xy(16,1,2,1000,0))
print(prob_xy(16,1,3,1000,0))
print(prob_xy(16,1,4,1000,0))
print(prob_xy(16,2,3,1000,0))
print(prob_xy(16,2,4,1000,0))
print(prob_xy(16,3,4,1000,0))
print('')
print(prob_xy(16,1,2,1000,1))
print(prob_xy(16,1,3,1000,1))
print(prob_xy(16,1,4,1000,1))
print(prob_xy(16,2,3,1000,1))
print(prob_xy(16,2,4,1000,1))
print(prob_xy(16,3,4,1000,1))
print('')
#print(table_edge_cpl(41))