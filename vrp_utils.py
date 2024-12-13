import networkx as nx
import itertools
import sys
import os
import json
import time


def load_graph(filename: str) -> nx.Graph:
    """
    Load a graph from a file.

    Parameters:
    filename (str): The name of the file

    Returns:
    graph (networkx.Graph): The loaded graph
    """
    graph = nx.Graph()
    with open(filename, "r") as file:
        for line in file:
            u, v, weight = line.strip().strip("()").split(", ")
            graph.add_edge(u, v, weight=int(weight))
    return graph

def calculate_route_cost(graph: nx.Graph, route: list) -> int:
    """
    Calculate the total cost of a given route.

    Parameters:
    graph (networkx.Graph): The graph
    route (list): The route

    Returns:
    cost (int): The total cost of the route
    """
    cost = 0
    for i in range(len(route) - 1):
        if route[i] in graph and route[i + 1] in graph[route[i]]:
            cost += graph[route[i]][route[i + 1]]['weight']
        else:
            # Jeśli krawędź nie istnieje, możesz dodać odpowiednią obsługę błędu
            # print(f"Brak krawędzi między {route[i]} a {route[i + 1]}")
            return sys.maxsize  # Zwróć maksymalny koszt, aby ta trasa nie była wybierana
    return cost


def save_results_to_json(results: dict, output_filename: str):
    """
    Save the results to a JSON file.

    Parameters:
    results (dict): The results to save
    output_filename (str): The name of the output file
    """
    with open(output_filename, "w") as json_file:
        json.dump(results, json_file, indent=4)
