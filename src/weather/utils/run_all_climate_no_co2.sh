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
    mkdir -p data/climate_no_co2/$scenario
    echo "Running scenario: $scenario"
    ./dcm_weather $scenario a.txt
    python3 ./clean_and_jsonize_output_no_co2.py $scenario
done

# mkdir -p ../../src/project/webapi/data/climate
# cp -r clean_data/climate ../../src/project/webapi/data
