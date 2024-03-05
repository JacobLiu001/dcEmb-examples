declare -a scenarios=(
    "ssp119"
    "ssp126"
    "ssp245"
    "ssp370"
    "ssp434"
    "ssp585"
    "ssp534-over"
)

echo "1.876 5.154 0.6435 2.632 9.262 52.93 1.285 2.691 0.4395 28.24 8" > a.txt

for scenario in "${scenarios[@]}"
do
    mkdir -p large_data/climate_no_co2/$scenario
    echo "Running scenario: $scenario"
    ./dcm_weather $scenario a.txt
    python3 ./clean_and_jsonize_output_large_no_co2.py $scenario
done

python3 ./split_json.py all

mkdir -p ../../src/project/webapi/static/large_data

mv ./clean_large_data/climate_no_co2 ../../src/project/webapi/static/large_data
mv ./split_data/climate2 ../../src/project/webapi/static/large_data

rm -r ./large_data
rm -r ./clean_large_data
rm -r ./split_data
