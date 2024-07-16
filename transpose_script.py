import argparse
import shutil
import scipy.io
import scipy.sparse as sp
from scipy.sparse import coo_matrix
from os import listdir
from os.path import isfile, join
import numpy as np
input_files = ["lp_scsd1", "bcsstm02"]

def get_all_files(path, file_names=None):
    if file_names is not None:
        with open(file_names, 'r') as file:
        # Read all lines into a list
            lines = file.readlines()
        onlyfiles = [f.replace("\n", ".mtx").replace(" ", "") for f in lines]
    else:
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f in onlyfiles:
        curr_files = [x for x in listdir("data/") if isfile(join("data/", x))]
        if f in curr_files:
            pass
        else:
            shutil.copy(join(path, f), "data/.")
    onlyfiles = [x.replace(".mtx", "") for x in onlyfiles if ".mtx" in x]
    #print(onlyfiles)
    return onlyfiles

def transpose_mtx(input_file, output_file, if_shift=True):
    # Read the matrix from the input .mtx file
    matrix = scipy.io.mmread(input_file)            
    # print(matrix)
    # Transpose the matrix
    print(input_file, type(matrix))
    if isinstance(matrix, np.ndarray):
        return
    if not sp.isspmatrix_coo(matrix):
        matrix = matrix.tocoo()
    # Get the matrix dimensions
    num_rows, num_cols = matrix.shape
    # Get the row, column, and data arrays
    rows, cols, data = matrix.row, matrix.col, matrix.data                                            
    print(min(rows), max(rows), num_rows)
    # Shift the row indices down by one position, wrapping around to the top
    print(min(cols), max(cols), num_cols)
    if if_shift:
       shifted_cols = (cols + 1) % num_cols
    else:
       shifted_cols = (cols) % num_cols
    shifted_rows = rows # (rows - 1) % num_rows
    # shifted_rows = (rows + 1) % num_rows
    
    shifted_matrix = sp.coo_matrix((data, (shifted_rows, shifted_cols)), shape=(num_rows, num_cols))
    shifted_matrix = shifted_matrix.transpose()                        
    # Create the shifted matrix using the updated row indices
    # Write the transposed matrix to the output .mtx file
    scipy.io.mmwrite(output_file, shifted_matrix)                                    
    print("cjheck")
    print(f"Transposed matrix saved to {output_file}")

parser = argparse.ArgumentParser()
parser.add_argument("--mode", help="An integer will be increased by 1 and printed.", type=int)
parser.add_argument("--file_path", help="An integer will be increased by 1 and printed.", type=str)
parser.add_argument("--files", help="An integer will be increased by 1 and printed.", type=str)
args = parser.parse_args()

print("mode is ", args.mode)

if args.mode == 1:
    path = "../../simulator/sweep_synthetics_25000/reorder_block/sam/data/suitesparse/"
    input_files.extend(get_all_files(path))
elif args.mode == 2:
    print(args.file_path, args.files)
    path = args.file_path
    input_files.extend(get_all_files(path, args.files))


for input_file in input_files:
    input_file_real = path + input_file
    output_file1 = "data/" + input_file + "_shifted.mtx"
    output_file2 = "data/" + input_file + "_transposed.mtx"
    input_file_real += ".mtx"
    transpose_mtx(input_file_real, output_file1)
    transpose_mtx(input_file_real, output_file2, if_shift=False)

input_file = "test_amazon0302"
input_file_real = "data/" + input_file
output_file = "data/" + input_file + "_shifted.mtx"
input_file_real += ".mtx"
transpose_mtx(input_file_real, output_file)
