# DRT
First follow the isntructions below to setup and run DRT.
Simulators for dynamic reflexive tiling and several accelerators.

Setup:
1. In `src/makefile` set the variable `MKLROOT` to your MKL library location
2. `src/makefile` contains the various targets. The relevant ones are:
    - SpMSpM_ExTensor: executable for the ExTensor simulation
    - SpMSpM_TACTile_twoInp: executable for the TACTile simulation
        - has options for static tiling and DRT tiling
    - SpMSpM_OuterSpace: executable for the idealized OuterSPACE untiled baseline
    - SpMSpM_OuterSpace_drt: executable for the idealized OuterSPACE baseline + DRT (with SUC options)
    - SpMSpM_MatRaptor: executable for the idealized MatRaptor untiled baseline
    - SpMSpM_MatRaptor_drt: executable for the idealized MatRaptor baseline + DRT (with SUC options)
3. To run the TACTile simulation (this assumes A is an IxJ matrix, B is a JxK matrix, and C is an IxK matrix):
    ```
    src/SpMSpM_TACTile_twoInp -inp1=<path to first matrix> -inp2=<path to second matrix> 
     --tiledim=<micro tile dimension> 
     --staticdist=<rr|nnz|oracle>  # static distributor for the PEs 
     --intersect=<skip|parbi>  #skip --> ExTensor skip-based intersection, parbi --> TACTile cfi/parallel intersection unit \
	 --tiling=<static|dynamic> 
	 --aperc=0.05  # LLB percentage assigned for tensor a
	 --bperc=0.35  # LLB percentage assigned for tensor b 
	 --operc=0.6   # LLB percentage assigned for tensor o 
     --llbsize=30  # LLB total size (in MB)
	 --constreuse=128 # # of micro tiles in a macro tile along the K dimension 
	 --topbw=68.25   # Top DOT (DRAM) bandwidth in GB/s 
	 --middlebw=2048 # Middle DOT NoC Bandwidth in GB/s 
	 --itop= # num. of microtiles in a macrotile along the I dimension for SUC tiling 
	 --jtop= # num. of microtiles in a macrotile along the J dimension for SUC tiling 
	 --ktop= # num. of microtiles in a macrotile along the K dimension for SUC tiling
    ```
    - An example command run: 
        - `src/SpMSpM_TACTile_twoInp --inp1=./data/test_amazon0302.mtx --inp2=./data/test_amazon0302.mtx --tiledim=32 --staticdist=rr --intersect=parbi --tiling=dynamic | tee out.txt`
        - 30MB is the default LLB size
        - llb default partitioning: A = 5%, B=50%, C=45%

4. To run the ExTensor simulation:
        - `src/SpMSpM_ExTensor --inp1=./data/test_amazon0302.mtx --inp2=./data/test_amazon0302.mtx --tiledim=32 --staticdist=rr --tiling=static --itop=32 --jtop=32 --ktop-32 | tee out.txt`

5. If you are using slurm, you can use the python scripts in the `run_...` directories to launch similar runs as those found in the paper. Please replace the DATADIR, OUTDIR, and EXECDIR with your local file paths (to your dataset directory of mtx files, the output directory where you want results, and the directory of your executable, respectively). You can also use the `slurmtest.py` files to see example launch commands and configurations. 



The tests can be run with run.sh that will generate logs for A * A and A * A^{T}' where A' is the matrix A shifted by 1 element.
Running result\_parser.py will extract the traffic logged by the DRT simulator.
*** 


