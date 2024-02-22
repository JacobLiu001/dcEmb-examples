declare -a xs=(
    "0.0"
    "0.1"
    "0.2"
    "0.3"
    "0.4"
    "0.5"
    "0.6"
    "0.7"
)

for x in "${xs[@]}"
do
    mkdir -p data/3body/$x
    echo "Running 3body with x: $x"
    ./dcm_3body $x
    python3 ./jsonize_3body.py $x
done

# mkdir -p ../../src/project/webapi/data/3body
# cp -r clean_data/3body ../../src/project/webapi/data
