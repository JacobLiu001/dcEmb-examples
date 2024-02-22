import csv
import json
import itertools
from argparse import ArgumentParser
from pathlib import Path

objects = ['A', 'B', 'C']
parameters = [
    'planet_masses',
    'planet_coordsX',
    'planet_coordsY',
    'planet_coordsZ',
    'planet_velocityX',
    'planet_velocityY',
    'planet_velocityZ'
]

column_names = [f"{param}_{obj}" for obj, param in itertools.product(objects, parameters)]

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    data = {
        column_name: [float(row[i]) for row in data] for i, column_name in enumerate(column_names)
    }
    
    with open(json_file, 'w') as f:
        json.dump(data, f)


def main(x: str):
    csv_filename = Path(f"data") / "3body" / f"{x}" / "deriv_generative.csv"
    json_filename = Path(f"clean_data") / "3body" / f"{x}" / "deriv_generative.json"
    json_filename.parent.mkdir(parents=True, exist_ok=True)
    csv_to_json(csv_filename, json_filename)

if __name__ == '__main__':
    parser = ArgumentParser(
        prog="jsonize_3body",
        description="Clean and convert data to JSON",
    )
    parser.add_argument(
        "x",
        type=str
    )
    args = parser.parse_args()
    main(args.x)