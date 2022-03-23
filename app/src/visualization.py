from networkx.classes.graph import Graph
from itertools import count
import networkx as nx
import matplotlib.pyplot as plt
import os

from classes import LastModification


def print_with_labels(graph: Graph, vector, file_name):
    t1_attributes = {}
    for node in graph.nodes:
        t1_attributes[node] = vector[node-1]
    nx.draw(graph, with_labels=True, labels=t1_attributes)
    # nx.draw_circular(graph, with_labels=True, labels=t1_attributes)
    plt.draw()
    plt.savefig(f"{file_name}.png")
    plt.clf()


# https://stackoverflow.com/a/28916094
def colormap(graph: Graph, attributes, file_name: str):
    groups = set(attributes)
    mapping = dict(zip(sorted(groups), count()))
    nodes = graph.nodes()
    colors = [mapping[attributes[n]] for n in nodes]

    # drawing nodes and edges separately so we can capture collection for colobar
    pos = nx.circular_layout(graph)
    ec = nx.draw_networkx_edges(graph, pos, alpha=0.2)
    nc = nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_color=colors,
                                node_size=100, cmap=plt.cm.jet)
    # TODO possible upgrade: node_size=[v * 100 for v in nodes.values()
    plt.colorbar(nc)
    plt.axis('off')
    plt.savefig(f"{file_name}.png")
    plt.clf()


def draw_iteration_result(graph: Graph, path: str, iteration: str, value, last_modification: LastModification, success: bool):
    if not os.path.exists(path):
        os.makedirs(path)

    if last_modification != None:
        edge_color_list = []
        if (success and not last_modification.is_add) or not success:
            graph.add_edge(last_modification.u,
                           last_modification.v)
        for e in graph.edges():
            if (e[0] == last_modification.u and e[1] == last_modification.v) or (e[1] == last_modification.u and e[0] == last_modification.v):
                if last_modification.is_add:
                    edge_color_list.append("limegreen")
                else:
                    edge_color_list.append("red")
            else:
                edge_color_list.append("black")

        node_color_list = []
        for n in graph.nodes():
            if n == last_modification.u or n == last_modification.v:
                if last_modification.is_add:
                    node_color_list.append("green")
                else:
                    node_color_list.append("darkred")
            else:
                node_color_list.append("tab:blue")

    else:
        edge_color_list = None
        node_color_list = None

    plt.title(f"{iteration}. iteration, {value}",
              color=("g" if success else "r"))
    nx.draw_circular(graph, edge_color=edge_color_list,
                     node_color=node_color_list)
    plt.savefig(f"{path}/{iteration}.png")
    plt.clf()