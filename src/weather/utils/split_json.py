import json
from pathlib import Path
from itertools import product
from argparse import ArgumentParser

YEARS = range(1750, 2101)
SCENARIOS = [
    'ssp119', 
    'ssp126', 
    'ssp245', 
    'ssp370', 
    'ssp434', 
    'ssp534-over', 
    'ssp585'
]
SPECIES = ['CO2', 'CH4', 'N2O']
METRICS = ['emissions', 'concentration', 'forcing', 'airborne_emissions']
COLUMNS = [f"{species}_{metric}" for species, metric in product(SPECIES, METRICS)]

def get_year_slice(year):
    offset = year - YEARS.start
    return slice(offset, -1, len(YEARS))

def detailed(input_dir: Path, output_dir: Path):
    data = json.loads(input_dir.read_text())
    for column in COLUMNS:
        for year in YEARS:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{year}" / f"{column}.json"
            sub_data = data[column][get_year_slice(year)]
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(json.dumps(sub_data))

def species(input_dir: Path, output_dir: Path):
    data = json.loads(input_dir.read_text())
    RUNS_TO_USE = 200
    for key in data:
        data[key] = data[key][:(RUNS_TO_USE * len(YEARS))]
    for specie in SPECIES:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{specie}.json"
        sub_data = {f"{specie}_{metric}": data[f"{specie}_{metric}"] for metric in METRICS}
        sub_data["run"] = data["run"]
        sub_data["year"] = data["year"]
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(json.dumps(sub_data))

def temperatures(input_dir: Path, output_dir: Path):
    data = json.loads(input_dir.read_text())
    RUNS_TO_USE = 200
    for key in data:
        data[key] = data[key][:(RUNS_TO_USE * len(YEARS))]

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"temps.json"
    sub_data = {key: data[key] for key in data if key.endswith("temp")}
    sub_data["run"] = data["run"]
    sub_data["year"] = data["year"]
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(sub_data))


def main(scenario: str, no_details: bool = False):
    INPUT_DIR = Path("clean_large_data/climate_no_co2") / scenario / "clean" / "pos_generative_rand.json"
    OUTPUT_DIR = Path("split_data/climate") / scenario
    if not no_details:
        detailed(INPUT_DIR, OUTPUT_DIR / "year")
    species(INPUT_DIR, OUTPUT_DIR / "species")
    temperatures(INPUT_DIR, OUTPUT_DIR / "temps")

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="split_json",
        description="Split json files into more manageable chunks for the server to statically serve.",
    )
    parser.add_argument(
        "scenario",
        type=str,
        help="The scenario to clean"
    )
    
    # yearly details is huge so we probably don't want to generate it every time
    parser.add_argument( 
        "--skip-yearly-details",
        dest="no_details",
        action="store_true",
        help="Skip splitting the yearly details"
    )
    args = parser.parse_args()
    scenario = args.scenario
    no_details = args.no_details
    if scenario == "all":
        for sc in SCENARIOS:
            main(sc, no_details)
    else:
        main(scenario, no_details)
