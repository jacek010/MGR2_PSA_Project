import json
import os
import matplotlib.pyplot as plt
import argparse as ap
import pandas as pd
import re
import sys

parser = ap.ArgumentParser(
    prog="VRP GA Create Plots",
    description="Create plots for genetic algorithm implementation results for VRP",
)


def add_arguments():
    parser.add_argument(
        "-i",
        "--results_folder",
        type=str,
        required=True,
        help="Paths to the folder with results JSON files",
    )
    parser.add_argument(
        "-p",
        "--parameter",
        type=str,
        required=True,
        choices=["p", "g", "m", "t"],
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


def extract_parameter_value_from_filename(filename: str, parameter_symbol: str) -> str:
    """
    Extract parameter value from the filename.

    Parameters:
    filename (str): The filename
    parameter_symbol (str): The symbol of the parameter to extract

    Returns:
    population (int): The extracted population value
    """
    match = re.search(rf"{parameter_symbol}(\d+)", filename)
    if match:
        return str(match.group(1))
    else:
        raise ValueError(f"Parameter value not found in filename: {filename}")


def load_results(
    results_folder: str, param_symbol: str, param_name: str
) -> pd.DataFrame:
    """
    Load results from multiple JSON files into a dataframe.

    Parameters:
    results_folder (str): Path to the results folder
    param_symbol (str): The symbol of the parameter to extract
    param_name (str): The name of the parameter

    Returns:
    df (DataFrame): The loaded results as a dataframe
    """
    filenames = [os.path.join(results_folder, f) for f in os.listdir(results_folder)]
    data = []
    for filename in filenames:
        param_value = extract_parameter_value_from_filename(filename, param_symbol)
        with open(filename, "r") as file:
            results = json.load(file)
            for result in results:
                nodes_count = result["nodes_count"]
                for vehicle_result in result["vehicles_amounts"]:
                    data.append(
                        {
                            "nodes_count": nodes_count,
                            "execution_time": vehicle_result["execution_time"],
                            "vehicles_amount": vehicle_result["vehicles_amount"],
                            param_name: param_value,
                        }
                    )
    df = pd.DataFrame(data)
    return df


def plot_execution_time_vs_nodes(
    df: pd.DataFrame, param_name: str, output_filename: str, plot_title: str
):
    """
    Plot the dependency of execution time on the number of nodes for each population value.

    Parameters:
    df (DataFrame): The dataframe containing the results to plot
    param_name (str): The name of the parameter
    output_filename (str): The path to save the plot
    plot_title (str): The title of the plot
    """
    df = df[df["vehicles_amount"] == 4]

    unique_param_values = df[param_name].unique()
    for param_val in unique_param_values:
        subset = df[df[param_name] == param_val]
        plt.plot(
            subset["nodes_count"],
            subset["execution_time"],
            label=f"{param_name} = {param_val}",
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.title(plot_title)
    plt.legend()
    plt.grid(True)
    plt.savefig(output_filename)
    plt.show()


if __name__ == "__main__":
    args = add_arguments()
    results_filenames = args.results_folder
    param_symbol = args.parameter
    output_graph = args.output
    plot_title = args.title

    match param_symbol:
        case "p":
            param_name = "population"
        case "m":
            param_name = "mutation_rate"
        case "g":
            param_name = "generations"
        case "t":
            param_name = "tournament_size"
        case _:
            raise ValueError(f"Invalid parameter symbol: {param_symbol}")

    results_df = load_results(results_filenames, param_symbol, param_name)
    plot_execution_time_vs_nodes(results_df, param_name, output_graph, plot_title)
