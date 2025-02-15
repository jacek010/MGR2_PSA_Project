import networkx as nx
import itertools
import sys
import os
import json
import time
from vrp_utils import load_graph, calculate_route_cost, save_results_to_json

INPUT_GRAPHS = "5-1000_1"
INPUT_DIR = f"graphs/{INPUT_GRAPHS}"

OUTPUT_FILENAME = f"results/{INPUT_GRAPHS}_BF.json"

VEHICLES_AMOUNTS = [1, 2, 3, 4]



def vrp_bruteforce(graph: nx.Graph, vehicles_amount: int) -> tuple:
    """
    Solve the Vehicle Routing Problem using brute force.

    Parameters:
    graph (networkx.Graph): The graph
    vehicles_amount (int): The number of vehicles

    Returns:
    best_routes (list of lists): The best routes for each vehicle
    best_cost (int): The total cost of the best routes
    """
    nodes = list(graph.nodes)
    nodes.remove('A')  # Remove 'A' from nodes to ensure it is only used as start and end
    best_cost = sys.maxsize
    best_routes = None

    for perm in itertools.permutations(nodes):
        routes = [['A'] + list(perm[i::vehicles_amount]) + ['A'] for i in range(vehicles_amount)]
        cost = sum(calculate_route_cost(graph, route) for route in routes)
        if cost < best_cost:
            best_cost = cost
            best_routes = routes

    return best_routes, best_cost


if __name__ == "__main__":
    results = []

    # Initialize the JSON file
    save_results_to_json(results, OUTPUT_FILENAME)
    
    for f in sorted(os.listdir(INPUT_DIR)):
        graph_filename = os.path.join(INPUT_DIR, f)
        print(f"Processing {graph_filename}")
        # Load the graph
        graph = load_graph(graph_filename)
        vehicles_results = []
        for vehicles_amount in VEHICLES_AMOUNTS:
            start_time = time.time()
            # Solve VRP using brute force
            best_routes, best_cost = vrp_bruteforce(graph, vehicles_amount)
            end_time = time.time()
            execution_time = end_time - start_time

            # Print the best routes, their cost, and execution time
            print(f"Best routes: {best_routes}")
            print(f"Total cost: {best_cost}")
            print(f"Vehicles amount: {vehicles_amount}")
            print(f"Execution time: {execution_time} seconds\n")
            
            vehicles_results.append({
                "vehicles_amount": vehicles_amount,
                "execution_time": execution_time,
                "best_routes": best_routes,
                "total_cost": best_cost
            })

            # Save the results
            results.append({
                "name": graph_filename,
                "nodes_count": graph.number_of_nodes(),
                "edges_count": graph.number_of_edges(),
                "vehicles_amounts": vehicles_results
            })

        # Append the results to the JSON file
        save_results_to_json(results, OUTPUT_FILENAME)

