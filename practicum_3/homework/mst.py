from typing import Any
from heapq import heappush, heappop
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting import plot_graph


def prim_mst(G: nx.Graph, start_node="0") -> set[tuple[Any, Any]]:
    mst_set = set()  # set of nodes included into MST
    rest_set = set(G.nodes())  # set of nodes not yet included into MST
    mst_edges = set()  # set of edges constituting MST

    # binary tree
    heap = []
    for neighbor, weight in G[start_node].items():
        heappush(heap, (weight["weight"], (start_node, neighbor)))

    # prime's algorithm
    while rest_set:

        current_distance, current_edge = heappop(heap)

        if current_edge[1] in mst_set:
            continue

        mst_edges.add(current_edge)
        mst_set.add(current_edge[1])
        rest_set.remove(current_edge[1])

        # add the neighbors of the current node to the heap
        for neighbor, weight in G[current_edge[1]].items():
            if neighbor in rest_set:
                heappush(heap, (weight["weight"], (current_edge[1], neighbor)))

    return mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    mst_edges = prim_mst(G, start_node="0")
    plot_graph(G, highlighted_edges=list(mst_edges))