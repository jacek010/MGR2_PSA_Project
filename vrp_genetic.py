import networkx as nx
import random
import os
import json
import time

from vrp_utils import (
    load_graph,
    calculate_route_cost,
    save_results_to_json,
    get_route,
    get_routes,
    couple_routes,
    decouple_routes,
)

# GENETIC PARAMS
# POPULATION_SIZE = 100
# GENERATIONS = 500
# MUTATION_RATE = 0.01
# TOURNAMENT_SIZE = 5

# INPUT PARAMS
INPUT_GRAPHS = "5-1000_1"
INPUT_DIR = f"graphs/{INPUT_GRAPHS}"
# OUTPUT_FILENAME = f"results/{INPUT_GRAPHS}_GA_p{POPULATION_SIZE}_g{GENERATIONS}_m{str(MUTATION_RATE).replace('.','')}_t{TOURNAMENT_SIZE}.json"
VEHICLES_AMOUNTS = [4]

REPETETIONS = 1


def set_default_values():
    global POPULATION_SIZE
    global GENERATIONS
    global MUTATION_RATE
    global TOURNAMENT_SIZE

    POPULATION_SIZE = 100
    GENERATIONS = 500
    MUTATION_RATE = 0.2
    TOURNAMENT_SIZE = 15


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
    nodes.remove("A")  # Remove the depot node
    population = []
    for _ in range(POPULATION_SIZE):
        random.shuffle(nodes)  # Shuffle the nodes randomly
        routes = [nodes[i::vehicles_amount] for i in range(vehicles_amount)]
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
    if len(population) < TOURNAMENT_SIZE:
        raise ValueError("Population size is smaller than tournament size")

    selected = random.sample(population, TOURNAMENT_SIZE)  # Randomly select individuals
    best_individual = min(selected, key=lambda x: x[1])[
        0
    ]  # Return the individual with the best fitness
    # print(f"best_individual{best_individual}")
    if not best_individual:
        raise ValueError("Selected individual is empty")

    return best_individual


def crossover(parent1: list, parent2: list) -> tuple:
    """
    Perform crossover between two parents to produce two children.

    This function combines routes from two parents to create two new child routes.

    Args:
        parent1 (list): The first parent.
        parent2 (list): The second parent.

    Returns:
        tuple: Two children produced from the crossover.
    """
    child1 = []
    child2 = []

    vehicles_routes_lengths, parent1_routes = couple_routes(parent1)
    vehicles_routes_lengths2, parent2_routes = couple_routes(parent2)

    # print(f"p1{parent1_routes}")
    # print(f"p2{parent2}")

    crossover_point = random.randint(1, len(parent1_routes) - 1)

    # CROSSOVER
    child_route1 = order_crossover(parent1_routes, parent2_routes)
    child_route2 = order_crossover(parent2_routes, parent1_routes)

    child1 = decouple_routes(vehicles_routes_lengths, child_route1)
    child2 = decouple_routes(vehicles_routes_lengths, child_route2)

    return child1, child2


def order_crossover(p1, p2):
    """
    Perform order crossover between two parents to produce a child.

    This function combines routes from two parents to create a new child route.

    """
    size = len(p1)
    child = [None] * size

    # Choose two random points for the crossover
    start, end = sorted(random.sample(range(size), 2))

    # Copy the segment from the first parent to the child
    child[start:end] = p1[start:end]

    # Fill the remaining positions with nodes from the second parent
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while p2[p2_index] in child:
                p2_index += 1
            child[i] = p2[p2_index]

    return child


def mutate(chromosome: list) -> list:
    """
    Mutate a given chromosome with a certain mutation rate.

    This function randomly swaps two nodes in the chromosome to introduce variation.

    Args:
        chromosome (list): The chromosome to mutate.

    Returns:
        list: The mutated chromosome.
    """
    vehicles_routes_lengths, coupled_routes = couple_routes(chromosome)
    if random.random() < MUTATION_RATE:
        if len(coupled_routes) > 2:  # Ensure there are enough nodes to swap
            i = random.randint(0, len(coupled_routes) - 1)
            j = random.randint(0, len(coupled_routes) - 1)
            coupled_routes[i], coupled_routes[j] = (
                coupled_routes[j],
                coupled_routes[i],
            )  # Swap two nodes
    chromosome = decouple_routes(vehicles_routes_lengths, coupled_routes)
    return chromosome


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
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        population = new_population
    best_routes, best_cost = evaluate_population(graph, population)[0]
    return best_routes, best_cost


def main():
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
            best_cost_sum = 0
            execution_time_sum = 0
            for _ in range(0, REPETETIONS):
                start_time = time.time()
                # Solve VRP using genetic algorithm
                best_routes, best_cost = genetic_algorithm(graph, vehicles_amount)
                end_time = time.time()

                best_cost_sum += best_cost
                execution_time_sum += end_time - start_time

            best_cost = best_cost_sum / REPETETIONS
            execution_time = execution_time_sum / REPETETIONS

            # Print the best routes, their cost, and execution time
            print(f"Best routes: {get_routes(best_routes)}")
            print(f"Total cost: {best_cost}")
            print(f"Vehicles amount: {vehicles_amount}")
            print(f"Execution time: {execution_time} seconds\n")

            vehicles_results.append(
                {
                    "vehicles_amount": vehicles_amount,
                    "execution_time": execution_time,
                    "best_routes": get_routes(best_routes),
                    "total_cost": best_cost,
                }
            )

            # Save the results
            results.append(
                {
                    "name": graph_filename,
                    "nodes_count": graph.number_of_nodes(),
                    "edges_count": graph.number_of_edges(),
                    "vehicles_amounts": vehicles_results,
                }
            )

        # Append the results to the JSON file
        save_results_to_json(results, OUTPUT_FILENAME)


if __name__ == "__main__":

    # Reset default values
    set_default_values()
    
    # OUTPUT_FILENAME = f"results/{INPUT_GRAPHS}_GA_p{POPULATION_SIZE}_g{GENERATIONS}_m{str(MUTATION_RATE).replace('.','')}_t{TOURNAMENT_SIZE}.json"
    # main()

    # TEST TOURNAMENT SIZES
    TOURNAMENT_SIZES = [2, 5, 10, 15, 20, 30]
    for t in TOURNAMENT_SIZES:
        print(f"MEASURING PARAMETER - Tournament size: {t}")
        TOURNAMENT_SIZE = t
        OUTPUT_FILENAME = f"results/tournament_test_new/{INPUT_GRAPHS}_GA_p{POPULATION_SIZE}_g{GENERATIONS}_m{str(MUTATION_RATE).replace('.','')}_t{TOURNAMENT_SIZE}.json"
        main()

    # # Reset default values
    # set_default_values()

    # # TEST POPULATION SIZES
    # POPULATION_SIZES = [10, 50, 100, 200]
    # for p in POPULATION_SIZES:
    #     POPULATION_SIZE = p
    #     OUTPUT_FILENAME = f"results/population_test/{INPUT_GRAPHS}_GA_p{POPULATION_SIZE}_g{GENERATIONS}_m{str(MUTATION_RATE).replace('.','')}_t{TOURNAMENT_SIZE}.json"
    #     main()

    # Reset default values
    set_default_values()

    # TEST GENERATIONS
    GENERATIONS_AMOUNTS = [50, 100, 200, 500, 1000, 2000]
    for g in GENERATIONS_AMOUNTS:
        print(f"MEASURING PARAMETER - Generations: {g}")
        GENERATIONS = g
        OUTPUT_FILENAME = f"results/generations_test_new/{INPUT_GRAPHS}_GA_p{POPULATION_SIZE}_g{GENERATIONS}_m{str(MUTATION_RATE).replace('.','')}_t{TOURNAMENT_SIZE}.json"
        main()

    # Reset default values
    set_default_values()

    # TEST MUTATION RATES
    MUTATION_RATES = [0.001, 0.01, 0.1, 0.2, 0.5]
    for m in MUTATION_RATES:
        print(f"MEASURING PARAMETER - Mutation rate: {m}")
        MUTATION_RATE = m
        OUTPUT_FILENAME = f"results/mutation_test_new/{INPUT_GRAPHS}_GA_p{POPULATION_SIZE}_g{GENERATIONS}_m{str(MUTATION_RATE).replace('.','')}_t{TOURNAMENT_SIZE}.json"
        main()
