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
        "--results",
        type=str,
        required=True,
        help="Paths to the folder with results JSON files",
    )
    parser.add_argument(
        "-p",
        "--parameter",
        type=str,
        required=True,
        choices=["p", "g", "m", "t", "i", "v", "a"],
    )
    parser.add_argument(
        "-v",
        "--vehicles_amount",
        type=int,
        default=4,
        help="Vehicle amount(s) to plot",
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="Path to the output PNG file"
    )
    parser.add_argument(
        "-y",
        "--y_axis",
        type=str,
        default="execution_time",
        choices=["execution_time", "total_cost"],
        help="Y axis variable",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=str,
        default="linear",
        choices=["linear", "log"],
        help="Y axis scale",
    )
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        default="VRP GA Execution Time vs Nodes",
        help="Plot title",
    )

    return parser.parse_args()


def extract_parameter_value_from_filename(
    filename: str, parameter_symbol: str
) -> int | float:
    """
    Extract parameter value from the filename.

    Parameters:
    filename (str): The filename
    parameter_symbol (str): The symbol of the parameter to extract

    Returns:
    population (int | float | str): The extracted parameter value
    """
    if parameter_symbol == "a":
        match = re.search(rf"{parameter_symbol}-(\w+)", filename)
    else:
        match = re.search(rf"{parameter_symbol}(\d+)", filename)
    if match:
        value = match.group(1)
        if value.startswith("0") and len(value) > 1:
            return float(f"0.{value[1:]}")
        elif parameter_symbol == "a":
            return str(value)
        else:
            return int(value)
    else:
        raise ValueError(f"Parameter value not found in filename: {filename}")


def load_results(
    results: str, param_symbol: str, param_name: str, y_var: str
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
    if os.path.isdir(results):
        filenames = [os.path.join(results, f) for f in os.listdir(results)]
    else:
        filenames = [results]
    data = []
    for filename in filenames:
        if param_symbol != "v":
            param_value = extract_parameter_value_from_filename(filename, param_symbol)
        with open(filename, "r") as file:
            results = json.load(file)
            for result in results:
                nodes_count = result["nodes_count"]
                for vehicle_result in result["vehicles_amounts"]:
                    entry = {
                        "nodes_count": nodes_count,
                        y_var: vehicle_result[y_var],
                        "vehicles_amount": vehicle_result["vehicles_amount"],
                    }
                    if param_symbol != "v":
                        entry[param_name] = param_value
                    data.append(entry)
    df = pd.DataFrame(data)
    df = df.sort_values(by=[param_name, "nodes_count"])
    return df


def plot_results(
    df: pd.DataFrame,
    param_name: str,
    vehicles_amount: int,
    output_filename: str,
    y_var: str,
    y_label: str,
    y_scale: str,
    plot_title: str,
):
    """
    Plot the dependency of execution time or total_cost on the number of nodes for each population value.

    Parameters:
    df (DataFrame): The dataframe containing the results to plot
    param_name (str): The name of the parameter
    output_filename (str): The path to save the plot
    y_var (str): The variable to plot on the y-axis
    y_label (str): The label for the y-axis
    y_scale (str): The scale for the y-axis
    plot_title (str): The title of the plot
    """
    if param_name != "vehicles_amount":
        df = df[df["vehicles_amount"] == vehicles_amount]

    unique_param_values = df[param_name].unique()
    for param_val in unique_param_values:
        subset = df[df[param_name] == param_val]
        plt.plot(
            subset["nodes_count"],
            subset[y_var],
            label=f"{param_name} = {param_val}",
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.legend()
    plt.yscale(y_scale)
    plt.grid(True)
    plt.savefig(output_filename)
    plt.show()


if __name__ == "__main__":
    args = add_arguments()
    results: str = args.results
    param_symbol: str = args.parameter
    vehicles_amount: int = args.vehicles_amount
    output_graph: str = args.output
    y_var: str = args.y_axis
    y_scale: str = args.scale
    plot_title: str = args.title

    match param_symbol:
        case "p":
            param_name = "population"
        case "m":
            param_name = "mutation_rate"
        case "g":
            param_name = "generations"
        case "t":
            param_name = "tournament_size"
        case "i":
            param_name = "iterations"
        case "v":
            param_name = "vehicles_amount"
        case "a":
            param_name = "algorithm"
        case _:
            raise ValueError(f"Invalid parameter symbol: {param_symbol}")

    match y_var:
        case "execution_time":
            y_label = "Execution Time (s)"
        case "total_cost":
            y_label = "Total Cost"
        case _:
            raise ValueError(f"Invalid y-axis variable: {y_var}")

    results_df = load_results(results, param_symbol, param_name, y_var)
    plot_results(
        results_df,
        param_name,
        vehicles_amount,
        output_graph,
        y_var,
        y_label,
        y_scale,
        plot_title,
    )
