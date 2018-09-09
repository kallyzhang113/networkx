import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import json
import random
from copy import deepcopy

def load_data(path):
    data = []
    count = -1
    with open(path, 'r') as rf:
        for line in rf.readlines():
            count += 1
            #if count == 500:
            #    break
            data.append(json.loads(line.strip()))
    print len(data), "data loaded."
    return data

def G_add_node(G, data):
    for d in data:
        if d['is_suspicious']:
            G.add_node(d['id'], is_suspicious=d['is_suspicious'], color='orange')
        else:
            G.add_node(d['id'], is_suspicious=d['is_suspicious'], color='steelblue')
    print G.number_of_nodes(), "nodes added."
    return G


def G_add_edge(G, data):
    for d in data:
        #source, sink
        if d['is_suspicious']:
            continue
        sink = d['id']
        node_type = nx.get_node_attributes(G, 'is_suspicious')
        for f in d['followers_list']:
            source = f['id']

            if source not in G.nodes():
                #continue
                G.add_node(source, is_suspicious=None, color='whitesmoke')
                G.add_edge(source, sink, color='whitesmoke')
            elif nx.get_node_attributes(G, 'is_suspicious')[source] == None:
                G.add_edge(source, sink, color='whitesmoke')
            elif node_type[sink] == True or node_type[source] == True:
                G.add_edge(source, sink, color='crimson')
            else:
                G.add_edge(source, sink, color='blue')
                G_plot(G)

    print G.number_of_edges(), "edges added."
    return G

def plot_connected_components(G):
    G_undirected = G.to_undirected()
    # layout graphs with positions using graphviz neato
    pos = graphviz_layout(G, prog="neato")
    # color nodes the same in each connected subgraph
    C = nx.connected_component_subgraphs(G_undirected)
    for g in C:
        g_directed = nx.DiGraph()
        for e in G.edges():
            if e[0] in g.nodes() and e[1] in g.nodes():
                g_directed.add_edge(e[0], e[1])
        c = [random.random()] * nx.number_of_nodes(g)  # random color...
        print c
        nx.draw(g_directed,
                pos,
                node_size=5,
                node_color=c,
                with_labels=False,
                width=0.2
               )
    plt.show()

def G_plot(G):
    # remove zerodegree
    zerodegree = [n for n in G if G.degree(n) == 0]
    for n in zerodegree:
        G.remove_node(n)

    pos = graphviz_layout(G, prog="neato")
    node_color = [nx.get_node_attributes(G, 'color')[n] for n in G.nodes()]
    edge_color = [nx.get_edge_attributes(G, 'color')[e] for e in G.edges()]
    nx.draw_networkx(
        G,
        pos,
        node_size=5,
        node_color=node_color,
        with_labels=False,
        width=0.2,
        edge_color=edge_color,
    )

    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    users = load_data('test.txt')
    G = nx.DiGraph()
    G = G_add_node(G, users)
    G = G_add_edge(G, users)

    G_plot(deepcopy(G))
