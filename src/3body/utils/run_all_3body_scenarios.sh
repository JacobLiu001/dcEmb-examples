declare -a xs=(
    "0.00"
    "0.01"
    "0.02"
    "0.03"
    "0.04"
    "0.05"
    "0.06"
    "0.07"
)

for x in "${xs[@]}"
do
    mkdir -p data/3body/$x
    echo "Running 3body with x: $x"
    ./dcm_3body $x
    python3 ./jsonize_3body.py $x
done

mkdir -p ../../src/project/webapi/data/3body
# cp -r clean_data/3body ../../src/project/webapi/data
