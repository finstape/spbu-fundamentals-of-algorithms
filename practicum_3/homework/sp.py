from typing import Any
import networkx as nx
from heapq import heappush, heappop

from src.plotting import plot_graph


def dijkstra_sp(G: nx.Graph, source_node="0") -> dict[Any, list[Any]]:
    shortest_paths = {}  # key = destination node, value = list of intermediate nodes
    distances = {vertex: float("inf") for vertex in G}
    distances[source_node] = 0
    heap = [(0, source_node)]

    # dijkstra algorithm based on binary heap
    while heap:
        current_distance, current_vertex = heappop(heap)

        if current_distance > distances[current_vertex]:
            continue

        # iterate over neighbors of current vertex to find minimum distance
        for neighbor, weight in G[current_vertex].items():
            new_distance = current_distance + weight["weight"]
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                shortest_paths[neighbor] = shortest_paths.get(current_vertex, []) + [current_vertex]
                heappush(heap, (new_distance, neighbor))

    # building the shortest path between two vertex
    shortest_paths[source_node] = [source_node]
    for vertex in G:
        if vertex != source_node:
            shortest_paths[vertex] += [vertex]

    return shortest_paths


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    shortest_paths = dijkstra_sp(G, source_node="0")
    test_node = "5"
    shortest_path_edges = [
        (shortest_paths[test_node][i], shortest_paths[test_node][i + 1])
        for i in range(len(shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)
