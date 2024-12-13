import networkx as nx
import random
import os
import json
import time

from vrp_utils import load_graph, calculate_route_cost, save_results_to_json

INPUT_GRAPHS = "5-1000_1"
INPUT_DIR = f"graphs/{INPUT_GRAPHS}"
OUTPUT_FILENAME = f"results/{INPUT_GRAPHS}_GA.json"
VEHICLES_AMOUNTS = [1, 2, 3, 4]

POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.01
TOURNAMENT_SIZE = 5


def create_initial_population(graph: nx.Graph, vehicles_amount: int) -> list:
    """
    Create the initial population for the genetic algorithm.

    This function generates a list of initial routes for the population by randomly shuffling the nodes
    and dividing them among the available vehicles.

    Args:
        graph (nx.Graph): The graph representing the VRP problem.
        vehicles_amount (int): The number of vehicles available.

    Returns:
        list: A list of initial routes for the population.
    """
    nodes = list(graph.nodes)
    nodes.remove('A')  # Remove the depot node
    population = []
    for _ in range(POPULATION_SIZE):
        random.shuffle(nodes)  # Shuffle the nodes randomly
        routes = [['A'] + nodes[i::vehicles_amount] + ['A'] for i in range(vehicles_amount)]
        population.append(routes)  # Create routes for each vehicle
    return population

def evaluate_population(graph: nx.Graph, population: list) -> list:
    """
    Evaluate the fitness of each individual in the population.

    This function calculates the total cost of each individual's routes and sorts the population
    based on the fitness scores (total cost).

    Args:
        graph (nx.Graph): The graph representing the VRP problem.
        population (list): The population to evaluate.

    Returns:
        list: A sorted list of tuples containing routes and their corresponding costs.
    """
    fitness_scores = []
    for routes in population:
        cost = sum(calculate_route_cost(graph, route) for route in routes)
        fitness_scores.append((routes, cost))  # Append the routes and their total cost
    return sorted(fitness_scores, key=lambda x: x[1])  # Sort by cost

def tournament_selection(population: list) -> list:
    """
    Select an individual using tournament selection.

    This function selects a subset of the population randomly and returns the individual with the best fitness.

    Args:
        population (list): The population from which to select.

    Returns:
        list: The selected individual.
    """
    selected = random.sample(population, TOURNAMENT_SIZE)  # Randomly select individuals
    return min(selected, key=lambda x: x[1])[0]  # Return the individual with the best fitness

def crossover(parent1: list, parent2: list) -> list:
    """
    Perform crossover between two parents to produce a child.

    This function combines routes from two parents to create a new child route.

    Args:
        parent1 (list): The first parent.
        parent2 (list): The second parent.

    Returns:
        list: The child produced from the crossover.
    """
    child = []
    for i in range(len(parent1)):
        route1 = parent1[i][1:-1]  # Remove 'A' from start and end
        route2 = parent2[i][1:-1]  # Remove 'A' from start and end
        child_route = []
        for j in range(len(route1)):
            if random.random() > 0.5:
                child_route.append(route1[j])  # Choose gene from first parent
            else:
                child_route.append(route2[j])  # Choose gene from second parent
        child.append(['A'] + child_route + ['A'])  # Add 'A' to start and end
    return child

def mutate(route: list) -> list:
    """
    Mutate a given route with a certain mutation rate.

    This function randomly swaps two nodes in the route to introduce variation.

    Args:
        route (list): The route to mutate.

    Returns:
        list: The mutated route.
    """
    for i in range(len(route)):
        if random.random() < MUTATION_RATE:
            if len(route[i]) > 3:  # Ensure there are enough nodes to swap
                j = random.randint(1, len(route[i]) - 2)
                route[i][j], route[i][j + 1] = route[i][j + 1], route[i][j]  # Swap two nodes
    return route

def genetic_algorithm(graph: nx.Graph, vehicles_amount: int) -> tuple:
    """
    Solve the VRP problem using a genetic algorithm.

    This function initializes the population, evaluates it, and iteratively performs selection,
    crossover, and mutation to evolve the population towards better solutions.

    Args:
        graph (nx.Graph): The graph representing the VRP problem.
        vehicles_amount (int): The number of vehicles available.

    Returns:
        tuple: The best routes and their total cost.
    """
    population = create_initial_population(graph, vehicles_amount)
    for _ in range(GENERATIONS):
        population = evaluate_population(graph, population)
        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        population = new_population
    best_routes, best_cost = evaluate_population(graph, population)[0]
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
            # Solve VRP using genetic algorithm
            best_routes, best_cost = genetic_algorithm(graph, vehicles_amount)
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
