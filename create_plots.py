import json
import matplotlib.pyplot as plt
import argparse as ap
import pandas as pd
import re

parser = ap.ArgumentParser(
    prog="VRP GA Create Plots",
    description="Create plots for genetic algorithm implementation results for VRP",
)

def add_arguments():
    parser.add_argument(
        "-i", "--results", type=str, nargs=4, required=True, help="Paths to the results JSON files"
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

def extract_population_from_filename(filename: str) -> int:
    """
    Extract the population value from the filename.

    Parameters:
    filename (str): The filename

    Returns:
    population (int): The extracted population value
    """
    match = re.search(r'p(\d+)', filename)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"Population value not found in filename: {filename}")

def load_results(filenames: list) -> pd.DataFrame:
    """
    Load results from multiple JSON files into a dataframe.

    Parameters:
    filenames (list): The list of filenames

    Returns:
    df (DataFrame): The loaded results as a dataframe
    """
    data = []
    for filename in filenames:
        population = extract_population_from_filename(filename)
        with open(filename, "r") as file:
            results = json.load(file)
            for result in results:
                nodes_count = result["nodes_count"]
                for vehicle_result in result["vehicles_amounts"]:
                    data.append({
                        "nodes_count": nodes_count,
                        "execution_time": vehicle_result["execution_time"],
                        "vehicles_amount": vehicle_result["vehicles_amount"],
                        "population": population
                    })
    df = pd.DataFrame(data)
    return df

def plot_execution_time_vs_nodes(df: pd.DataFrame, output_filename: str, plot_title: str):
    """
    Plot the dependency of execution time on the number of nodes for each population value.

    Parameters:
    df (DataFrame): The dataframe containing the results to plot
    """
    df = df[df["vehicles_amount"] == 4]

    unique_populations = df["population"].unique()
    for population in unique_populations:
        subset = df[df["population"] == population]
        plt.plot(subset["nodes_count"], subset["execution_time"], label=f"Population {population}")

    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.title(plot_title)
    plt.legend()
    plt.grid(True)
    plt.savefig(output_filename)
    plt.show()

if __name__ == "__main__":
    args = add_arguments()
    results_filenames = args.results
    output_graph = args.output
    plot_title = args.title

    results_df = load_results(results_filenames)
    plot_execution_time_vs_nodes(results_df, output_graph, plot_title)
