declare -a xs=(
    "0.04"
)

for x in "${xs[@]}"
do
    mkdir -p data/3body/$x
    echo "Running 3body with x: $x"
    ./dcm_3body $x
    # python3 ./clean_and_jsonize_output.py $scenario
done

cp -r data/3body clean_data/

mkdir -p ../../src/project/webapi/data/3body
cp -r clean_data/3body ../../src/project/webapi/data/3body
