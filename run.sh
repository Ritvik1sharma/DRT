
mkdir "logs_1_comp"
mkdir "logs_2_comp"

# python3 transpose_script.py --mode=2 --file_path="/nobackup/owhsu/sparse-datasets/suitesparse/" --files=$1
while read line; do
    echo ${SUITESPARSE_FORMATTED_PATH}${line}.mtx
    echo ./data/${line}_shifted.mtx
    
    src/SpMSpM_TACTile_twoInp --inp1="./data/"${line}".mtx" --inp2="./data/"${line}".mtx" \
	--tiledim=32 --staticdist=rr --intersect=parbi --tiling=dynamic | tee "logs_1_comp/"${line}"_dynamic.txt"
    src/SpMSpM_TACTile_twoInp --inp1="./data/"${line}".mtx" --inp2="./data/"${line}".mtx" \
	--tiledim=32 --staticdist=rr --intersect=parbi --tiling=static | tee "logs_1_comp/"${line}"_static.txt"
done <$1


while read line; do
    echo ${SUITESPARSE_FORMATTED_PATH}${line}.mtx
    echo ./data/${line}_shifted.mtx

    src/SpMSpM_TACTile_twoInp --inp1="./data/"${line}".mtx" --inp2="./data/"${line}"_shifted.mtx" \
	    --tiledim=32 --staticdist=rr --intersect=parbi --tiling=dynamic | tee "logs_2_comp/"${line}"_dynamic.txt"		src/SpMSpM_TACTile_twoInp --inp1="./data/"${line}".mtx" --inp2="./data/"${line}"_shifted.mtx" \
	    --tiledim=32 --staticdist=rr --intersect=parbi --tiling=static | tee "logs_2_comp/"${line}"_static.txt"
done <$1
