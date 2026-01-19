# TD-DFT Calculation Pipeline

This directory contains a refactored pipeline for performing TD-DFT calculations on single SMILES strings. The pipeline consists of four sequential steps, from initial 3D coordinate generation to final TD-DFT calculation.

## Pipeline Overview

1.  **SMILES to XYZ**: Generate initial 3D coordinates using RDKit (ETKDG + UFF optimization).
2.  **Pre-optimization**: Fast geometry optimization using ORCA with the GFN-xtB2 method.
3.  **Ground-State Optimization**: Full geometry optimization using Gaussian (B3LYP/6-31G*).
4.  **TD-DFT Calculation**: Excited state calculation using Gaussian (B3LYP/6-31G*, Nstates=1).

## Prerequisites

> [!IMPORTANT]
> This pipeline requires **ORCA** and **Gaussian** to be installed and configured in your environment.

-   **Python Packages**: `rdkit`, `ase`
-   **Quantum Chemistry Tools**:
    -   **[ORCA](https://www.faccts.de/orca/)**: Ensure the path is correctly configured in the scripts (default: `/appl/orca_4.2.1/orca_4_2_1_linux_x86-64_openmpi314/orca`). You may need to update this path in `2_pre_optimize.py`.
    -   **[Gaussian](https://gaussian.com/)**: The `g16` command must be available in your system's PATH.

## Scripts

### 1. `1_smiles_to_xyz.py`
Converts a SMILES string to an initial XYZ file.
```bash
python 1_smiles_to_xyz.py "SMILES" output.xyz
```

### 2. `2_pre_optimize.py`
Performs pre-optimization using ORCA GFN-xtB2.
```bash
python 2_pre_optimize.py input.xyz --out_dir ./output_dir --out_name molecule_name
```

### 3. `3_ground_state_opt.py`
Performs ground-state optimization using Gaussian B3LYP/6-31G*.
```bash
python 3_ground_state_opt.py input.xyz --out_dir ./output_dir --out_name molecule_name
```

### 4. `4_td_dft_calc.py`
Performs TD-DFT calculation using a Gaussian checkpoint file.
```bash
python 4_td_dft_calc.py input.chk --out_dir ./output_dir --out_name molecule_name
```

## Example Usage

### Single Molecule (`test.sh`)

A sample shell script `test.sh` is provided to run the full pipeline for a single molecule:

```bash
sbatch test.sh
```

### Batch Processing (`run_td_dft_batch.py`)

For processing multiple SMILES from a CSV file:

```bash
python run_td_dft_batch.py
```

This script reads SMILES from the CSV file, creates individual job scripts in `jobs/`, and submits them via `sbatch`. Results are stored in `results/{mol_id}/` for each molecule.
