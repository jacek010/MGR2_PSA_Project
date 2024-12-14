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
    route = get_route(route)
    for i in range(len(route) - 1):
        if route[i] in graph and route[i + 1] in graph[route[i]]:
            cost += graph[route[i]][route[i + 1]]['weight']
        else:
            # Jeśli krawędź nie istnieje, możesz dodać odpowiednią obsługę błędu
            # print(f"Brak krawędzi między {route[i]} a {route[i + 1]}")
            return sys.maxsize  # Zwróć maksymalny koszt, aby ta trasa nie była wybierana
    return cost

def get_route(route:list)->list:
    return ['A']+ route + ['A']

def get_routes(routes: list[list[str]]) -> list[list[str]]:
    return [get_route(route) for route in routes]

def couple_routes(routes: list[list[str]]) -> tuple:
    vehicles_routes_lengths = [len(routes[i]) for i in range(len(routes))]
    coupled_routes = [node for route in routes for node in route if node != 'A']
    
    return vehicles_routes_lengths, coupled_routes

def decouple_routes(vehicles_routes_lengths: list[int], coupled_routes: list[str]) -> list[list[str]]:
    routes = []
    start = 0
    for length in vehicles_routes_lengths:
        routes.append(coupled_routes[start:start+length])
        start += length
    return routes

def save_results_to_json(results: dict, output_filename: str):
    """
    Save the results to a JSON file.

    Parameters:
    results (dict): The results to save
    output_filename (str): The name of the output file
    """
    with open(output_filename, "w") as json_file:
        json.dump(results, json_file, indent=4)
