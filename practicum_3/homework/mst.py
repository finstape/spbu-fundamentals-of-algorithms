from typing import Any
from heapq import heappush, heappop
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting import plot_graph


def prim_mst(G: nx.Graph, start_node="0") -> set[tuple[Any, Any]]:
    mst_set = set()  # set of nodes included into MST
    rest_set = set(G.nodes())  # set of nodes not yet included into MST
    mst_edges = set()  # set of edges constituting MST
    mst_set.add(start_node)
    rest_set.remove(start_node)

    while rest_set:
        new_edge = {"edge": (None, None), "weight": float("inf")}

        # finding the minimum edge
        for vertex in mst_set:
            for neighbor, weight in G[vertex].items():
                if neighbor not in mst_set and weight["weight"] < new_edge["weight"]:
                    new_edge["edge"] = (vertex, neighbor)
                    new_edge["weight"] = weight["weight"]

        # minimal edge processing
        mst_set.add(new_edge["edge"][1])
        rest_set.remove(new_edge["edge"][1])
        mst_edges.add(new_edge["edge"])

    return mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    mst_edges = prim_mst(G, start_node="0")
    plot_graph(G, highlighted_edges=list(mst_edges))
