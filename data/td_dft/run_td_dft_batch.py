#!/usr/bin/env python
"""TD-DFT batch job submission script."""
import pandas as pd
import os
import subprocess

CSV_PATH = "./test_data.csv"
WORK_DIR = "./"

TEMPLATE = """#!/bin/bash
#SBATCH -J TD_{mol_id}
#SBATCH -p 16core
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time=1000:00:00
#SBATCH -o {work_dir}/logs/{mol_id}.out
#SBATCH -e {work_dir}/logs/{mol_id}.err

source /etc/profile.d/modules.sh
module load software_module/g16_B.01_AVX

cd {work_dir}

SMILES="{smiles}"
NAME="{mol_id}"
OUT_DIR="./results/{mol_id}"

mkdir -p "$OUT_DIR"

python 1_smiles_to_xyz.py "$SMILES" "$OUT_DIR/initial.xyz"
python 2_pre_optimize.py "$OUT_DIR/initial.xyz" --out_dir "$OUT_DIR" --out_name "pre_opt"
python 3_ground_state_opt.py "$OUT_DIR/pre_opt.xyz" --out_dir "$OUT_DIR" --out_name "opt"
python 4_td_dft_calc.py "$OUT_DIR/opt.chk" --out_dir "$OUT_DIR" --out_name "td"
"""

def main():
    df = pd.read_csv(CSV_PATH)
    os.makedirs(f"{WORK_DIR}/jobs", exist_ok=True)
    os.makedirs(f"{WORK_DIR}/logs", exist_ok=True)
    
    for _, row in df.iterrows():
        mol_id = f"mol_{row['MolID']}"
        smiles = row['SMILES']
        
        job_script = TEMPLATE.format(
            mol_id=mol_id, smiles=smiles, work_dir=WORK_DIR
        )
        
        job_path = f"{WORK_DIR}/jobs/{mol_id}.sh"
        with open(job_path, 'w') as f:
            f.write(job_script)
        
        subprocess.run(["sbatch", job_path])
        print(f"Submitted: {mol_id}")

if __name__ == "__main__":
    main()
