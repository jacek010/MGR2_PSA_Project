import networkx as nx
import random
import os

NODES_LIST = [5,6,7,8,9,10,11,12,13,14,15,17,20, 25, 35, 50, 57, 100, 200, 500, 1000]
GRAPH_DESITY = 1
MIN_WEIGHT = 50
MAX_WEIGHT = 200

GRAPHS_DIRECTORY = f"graphs/{NODES_LIST[0]}-{NODES_LIST[-1]}_{str(GRAPH_DESITY).replace('.', '')}"







def create_graph(edges:list)->nx.Graph:
    """
    Create an undirected graph with custom edge weights.

    Parameters:
    edges (list of tuples): Each tuple contains (node1, node2, weight)

    Returns:
    G (networkx.Graph): The generated graph
    """
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    return G

def generate_edges_with_weights(nodes:list)->list:
    """
    Generate a list of edges with random weights for a given list of nodes.

    Parameters:
    nodes (list): List of nodes
    max_weight (int): Maximum weight for the edges

    Returns:
    edges (list of tuples): Each tuple contains (node1, node2, weight)
    """
    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            weight = random.randint(MIN_WEIGHT, MAX_WEIGHT)
            edges.append((nodes[i], nodes[j], weight))
    return edges

def generate_nodes(n:int)->list:
    """
    Generate a list of nodes.

    Parameters:
    n (int): Number of nodes

    Returns:
    nodes (list): List of nodes
    """
    nodes = [chr(i) for i in range(65, 65 + n)]
    return nodes

def delete_random_edges(edges:list, x:int):
    """
    Delete x random edges from the list of edges.

    Parameters:
    edges (list of tuples): List of edges
    x (int): Number of edges to delete

    Returns:
    edges (list of tuples): List of edges after deletion
    """
    if x > len(edges):
        raise ValueError("Number of edges to delete exceeds the total number of edges")
    edges_to_delete = random.sample(edges, x)
    for edge in edges_to_delete:
        edges.remove(edge)
    return edges

def print_graph(graph:nx.Graph)->None:
    """
    Print the graph.

    Parameters:
    graph (networkx.Graph): The graph to print
    """
    for u, v, weight in graph.edges(data='weight'):
        print(f"({u}, {v}, {weight})")
        
def print_graph_to_file(graph:nx.Graph, filename:str)->None:
    """
    Print the graph to a file.

    Parameters:
    graph (networkx.Graph): The graph to print
    filename (str): The name of the file
    """
    with open (filename, "w") as file:
        for u, v, weight in graph.edges(data='weight'):
            file.write(f"({u}, {v}, {weight})\n")

def main():
    # Create directory if it doesn't exist
    if not os.path.exists(GRAPHS_DIRECTORY):
        os.makedirs(GRAPHS_DIRECTORY)

    for NODES in NODES_LIST:
        EDGES = NODES * (NODES - 1) // 2
        EDGES_TO_DELETE = round(EDGES * (1 - GRAPH_DESITY))
        # Generate nodes
        nodes = generate_nodes(NODES)
        
        # Generate edges with random weights
        edges = generate_edges_with_weights(nodes)
        
        # Delete random edges
        edges = delete_random_edges(edges, EDGES_TO_DELETE)
        
        # Create a graph
        graph = create_graph(edges)

        # Print the edges with weights
        # print_graph(graph)
        print_graph_to_file(graph, f"{GRAPHS_DIRECTORY}/graph_{NODES:03d}.txt")

if __name__ == "__main__":
    main()