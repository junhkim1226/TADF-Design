# Harnessing Generative AI for Efficient Organic Materials Discovery in Low-Data Regimes

Source code of "Harnessing Generative AI for Efficient Organic Materials Discovery in Low-Data Regimes"

## Environment

This code has been tested on **Ubuntu 22.04.2 LTS**.
We recommend using `conda` to manage the environment.

### Option 1: Using environment.yml (Recommended)
You can create the environment directly from the provided `environment.yml` file.
> [!NOTE]
> The `environment.yml` file includes `mkl==2023` to resolve potential `torch` import errors.

```bash
conda env create -f environment.yml
conda activate TADFGen
```

### Option 2: Manual Installation
Alternatively, you can install the requirements manually:
```bash
conda create -n TADFGen python=3.9
conda activate TADFGen
conda install pytorch=1.12.1 cudatoolkit=11.3 -c pytorch
pip install numpy==1.23.5
pip install hydra-core==1.1.0
pip install pandas rdkit=2024.9.6
pip install ase==3.26.0 # Required for td-dft calculation
```

> [!NOTE]
> If you encounter a `torch` import error related to MKL, please install `mkl` explicitly:
> ```bash
> conda install mkl==2023
> ```

## Data Processing

Our training data is available in `./data/TADF/property.db`. This database has already been processed and is ready for use.

> [!IMPORTANT]
> If you provide your own `property.db`, it must be a **CSV file** containing at least two columns:
> - `MolID`: Unique identifier for the molecule
> - `SMILES`: SMILES string of the molecule
>
> For **conditional generation**, the following property columns are also required:
> - `S1`: Singlet energy
> - `Est`: Singlet-Triplet energy gap

If you need to preprocess raw data yourself, run the following code. Please note that data processing may take a significant amount of time.
```bash
cd ./data
mkdir new_TADF
cp ./TADF/property.db ./new_TADF/property.db
./data_preprocess.sh new_TADF/ <cpus>
```

Preprocessed data will be available in `./data/new_TADF`.

## Model Training

To train the model, run the following commands:
```bash
cd ./result/
bash ./jobscript_train.sh
```

The training configuration (e.g., epochs, batch size) can be modified in `jobscript_train.sh`.

## Generating

You can generate molecules using the trained model with specific property conditions (e.g., Est, S1).
We provide example scripts for generating Blue, Green, and Red TADF candidates.
By default, a pre-trained model is provided in `result/Trained_Model/Est_S1/trained_model.tar`.


```bash
cd ./sample/
# For blue TADF candidates generation (Est=0.1, S1=2.73)
bash ./sample/jobscript_blue.sh

# For green TADF candidates generation (Est=0.1, S1=2.23)
bash ./sample/jobscript_green.sh

# For red TADF candidates generation (Est=0.1, S1=1.87)
bash ./sample/jobscript_red.sh
```

## DFT Data

The raw data used in this study, including generated candidates and training data, is stored in the `DFT_data` directory.
Please refer to [DFT_data/README.md](./DFT_data/README.md) for a detailed description of the files.

## TD-DFT Calculation

We provide a pipeline for performing TD-DFT calculations on the generated molecules.
The scripts are located in `data/td_dft`.
Please refer to [data/td_dft/README.md](./data/td_dft/README.md) for detailed instructions on setting up the environment (ORCA, Gaussian) and running the calculations.

## Contact

If you have any questions or issues, please contact:
**Jun Hyeong Kim** (junhkim1226@kaist.ac.kr)