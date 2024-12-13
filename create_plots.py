import json
import matplotlib.pyplot as plt

RESULTS_INSTANCE = "5-1000_1_GA"
RESULTS_FILENAME = f"results/{RESULTS_INSTANCE}.json"

PLOT_OUTPUT_FILENAME = f"images/plots/{RESULTS_INSTANCE}.png"

def load_results(filename: str) -> list:
    """
    Load results from a JSON file.

    Parameters:
    filename (str): The name of the file

    Returns:
    results (list): The loaded results
    """
    with open(filename, "r") as file:
        results = json.load(file)
    return results

def plot_execution_time_vs_nodes(results: list):
    """
    Plot the dependency of execution time on the number of nodes.

    Parameters:
    results (list): The results to plot
    """
    nodes_counts = []
    execution_times = []
    vehicles_amounts = []

    for result in results:
        nodes_count = result["nodes_count"]
        for vehicle_result in result["vehicles_amounts"]:
            nodes_counts.append(nodes_count)
            execution_times.append(vehicle_result["execution_time"])
            vehicles_amounts.append(vehicle_result["vehicles_amount"])

    # Plot each vehicle amount separately
    unique_vehicles_amounts = sorted(set(vehicles_amounts))
    for vehicles_amount in unique_vehicles_amounts:
        x = [nodes_counts[i] for i in range(len(nodes_counts)) if vehicles_amounts[i] == vehicles_amount]
        y = [execution_times[i] for i in range(len(execution_times)) if vehicles_amounts[i] == vehicles_amount]
        plt.plot(x, y, label=f'{vehicles_amount} vehicles')

    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Dependency of Execution Time on Number of Nodes\n for Different Vehicles Amounts using Bruteforce")
    # plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.savefig(PLOT_OUTPUT_FILENAME)
    plt.show()

if __name__ == "__main__":
    
    results = load_results(RESULTS_FILENAME)
    plot_execution_time_vs_nodes(results)
