from typing import Any
from heapq import heappush, heappop
import matplotlib.pyplot as plt
import networkx as nx

from src.plotting import plot_graph


def prim_mst(G: nx.Graph, start_node="0") -> set[tuple[Any, Any]]:
    mst_set = set()  # set of nodes included into MST
    rest_set = set(G.nodes())  # set of nodes not yet included into MST
    mst_edges = set()  # set of edges constituting MST
    heap = [(0, start_node, None)]

    # prime's algorithm
    while heap:
        _, current_vertex, predecessor = heappop(heap)

        if current_vertex not in rest_set:
            continue

        rest_set.remove(current_vertex)

        if predecessor is not None:
            mst_edges.add((current_vertex, predecessor))

        mst_set.add(current_vertex)

        # add the neighbors of the current node to the heap
        for neighbor, weight in G[current_vertex].items():
            if neighbor not in rest_set:
                continue
            heappush(heap, (weight["weight"], neighbor, current_vertex))

    return mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    mst_edges = prim_mst(G, start_node="0")
    plot_graph(G, highlighted_edges=list(mst_edges))
