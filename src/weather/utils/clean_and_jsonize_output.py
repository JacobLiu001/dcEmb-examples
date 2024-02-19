# Dependencies
import os
import pathlib
import json
import pandas as pd
from argparse import ArgumentParser

# Original code by Kai, refractored by Jacob to use pathlib instead of os

# Read in csv and return processed dataframe
def read_csv(file_name, dir, column_names, start_year, end_year):
    # Read the CSV into a pandas dataframe without headers
    file_path = dir / file_name
    df = pd.read_csv(file_path, header=None)

    # Rename columns in df
    df.columns = column_names

    # Add year column
    num_timestamps = end_year - start_year + 1
    df["year"] = (df.index % num_timestamps) + start_year
    return df


# Write dataframe to both csv and json output
def save(df, file_name, output_dir):
    output_csv_path = output_dir / "csv" / file_name
    df.to_csv(output_csv_path, index=False)
    output_json_path = (output_dir / file_name).with_suffix(".json")
    with open(output_json_path, "w") as file:
        json.dump({col: df[col].tolist() for col in df.columns}, file)


# Read "pos_generative.csv" and outputs formatted CSV and JSON
def clean_pos_generative(file_name, dir, output_dir, column_names, start_year, end_year):
    # Read in data
    df = read_csv(file_name, dir, column_names, start_year, end_year)

    # Remove all of the intermediate model data
    num_timestamps = end_year - start_year + 1
    df = df.tail(num_timestamps)

    # Write to output directory
    save(df, file_name, output_dir)


# Read pos_generative_rand.csv
def clean_pos_generative_rand(file_name, dir, output_dir, column_names, start_year, end_year, n):
    df = read_csv(file_name, dir, column_names, start_year, end_year)
    num_timestamps = end_year - start_year + 1
    df = df.tail(n * num_timestamps)
    df["run"] = ((df.index % (n * num_timestamps)) // num_timestamps) + 1  # each run is a different sampling of model params
    save(df, file_name, output_dir)


# Read "true_generative.csv"
def clean_true_generative(file_name, dir, output_dir, column_names, start_year, end_year):
    df = read_csv(file_name, dir, column_names, start_year, end_year)
    save(df, file_name, output_dir)


# Read "prior_generative.csv"
def clean_prior_generative(file_name, dir, output_dir, column_names, start_year, end_year):
    df = read_csv(file_name, dir, column_names, start_year, end_year)
    save(df, file_name, output_dir)


# Read "prior_generative_rand.csv" TODO
def clean_prior_generative_rand(file_name, dir, output_dir, column_names, start_year, end_year, n):
    df = read_csv(file_name, dir, column_names, start_year, end_year)
    num_timestamps = end_year - start_year + 1
    df["run"] = (df.index // num_timestamps) + 1  # each run is a different sampling
    save(df, file_name, output_dir)


def main(scenario):
    # Input directory
    input_dir = pathlib.Path(f"data/climate/") / scenario

    # DCM input data
    START_YEAR, END_YEAR = 1750, 2100
    N = 10  # No. samples
    SPECIES = ["CO2_FFI", "CO2_AFOLU", "CO2", "CH4", "N2O"]  # species list

    # Construct column names
    emissions_cols = [f"{s}_emissions" for s in SPECIES]
    concentrations_cols = [f"{s}_concentration" for s in SPECIES]
    forcings_cols = [f"{s}_forcing" for s in SPECIES]
    temp_cols = ["atmospheric_temp", "sea_layer1_temp", "sea_layer2_temp", "sea_layer3_temp"]
    airborne_emissions_cols = [f"{s}_airborne_emissions" for s in SPECIES]
    column_names = emissions_cols + concentrations_cols + forcings_cols + temp_cols + airborne_emissions_cols

    # Prepare output directory
    output_dir = pathlib.Path(f"clean_data/climate") / scenario / "clean"
    output_dir_csv = output_dir / "csv"
    output_dir_csv.mkdir(parents=True, exist_ok=True)

    # Parse and clean CSV data
    clean_pos_generative("pos_generative.csv", input_dir, output_dir, column_names, START_YEAR, END_YEAR)
    clean_pos_generative_rand("pos_generative_rand.csv", input_dir, output_dir, column_names, START_YEAR, END_YEAR, N)
    clean_true_generative("true_generative.csv", input_dir, output_dir, column_names, START_YEAR, END_YEAR)
    clean_prior_generative("prior_generative.csv", input_dir, output_dir, column_names, START_YEAR, END_YEAR)
    clean_prior_generative_rand("prior_generative_rand.csv", input_dir, output_dir, column_names, START_YEAR, END_YEAR, N)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="clean_and_jsonize_output",
        description="Clean and convert data to JSON",
    )
    parser.add_argument(
        "scenario",
        type=str,
        help="The scenario to clean"
    )
    args = parser.parse_args()
    main(args.scenario)
