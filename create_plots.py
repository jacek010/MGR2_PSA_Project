import json
import matplotlib.pyplot as plt
import argparse as ap

parser = ap.ArgumentParser(
    prog="VRP GA Create Plots",
    description="Create plots for genetic algorithm implementation results for VRP",
)


def add_arguments():
    parser.add_argument(
        "-i", "--results", type=str, required=True, help="Path to the results JSON file"
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="Path to the output PNG file"
    )
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        default="VRP GA Execution Time vs Nodes",
        help="Plot title",
    )

    return parser.parse_args()


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


def plot_execution_time_vs_nodes(results: list, output_filename: str, plot_title: str):
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
        x = [
            nodes_counts[i]
            for i in range(len(nodes_counts))
            if vehicles_amounts[i] == vehicles_amount
        ]
        y = [
            execution_times[i]
            for i in range(len(execution_times))
            if vehicles_amounts[i] == vehicles_amount
        ]
        plt.plot(x, y, label=f"{vehicles_amount} vehicles")

    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.title(plot_title)
    # plt.yscale("log")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_filename)
    plt.show()


if __name__ == "__main__":
    args = add_arguments()
    results_filename = args.results
    output_graph = args.output
    plot_title = args.title

    results = load_results(results_filename)
    plot_execution_time_vs_nodes(results, output_graph, plot_title)
