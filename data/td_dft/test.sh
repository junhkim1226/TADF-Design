#!/bin/bash
#SBATCH -J TD_DFT_TEST 
#SBATCH -p 16core
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time=1000:00:00
#SBATCH -o ./logs/test.out
#SBATCH -e ./logs/test.err

# Example script to run the full TD-DFT pipeline for a single SMILES string
source /etc/profile.d/modules.sh
module load software_module/g16_B.01_AVX

# SMILES="c1ccccc1"
SMILES="Cc1nc(C)c(C#N)c(C(C)(C)C)c1C#N"
NAME="blue_test"
OUT_DIR="./results"

# 1. SMILES to XYZ (RDKit UFF)
echo "Step 1: SMILES to XYZ..."
python 1_smiles_to_xyz.py "$SMILES" "${OUT_DIR}/${NAME}_initial.xyz"

# 2. Pre-optimization (ORCA GFN-xtB2)
echo "Step 2: Pre-optimization (ORCA)..."
python 2_pre_optimize.py "${OUT_DIR}/${NAME}_initial.xyz" --out_dir "$OUT_DIR" --out_name "${NAME}_pre_opt"

# 3. Ground-state Optimization (Gaussian B3LYP)
echo "Step 3: Ground-state Optimization (Gaussian)..."
python 3_ground_state_opt.py "${OUT_DIR}/${NAME}_pre_opt.xyz" --out_dir "$OUT_DIR" --out_name "${NAME}_opt"

# 4. TD-DFT Calculation (Gaussian)
echo "Step 4: TD-DFT Calculation (Gaussian)..."
python 4_td_dft_calc.py "${OUT_DIR}/${NAME}_opt.chk" --out_dir "$OUT_DIR" --out_name "${NAME}_td"

echo "Pipeline completed. Results are in $OUT_DIR"
