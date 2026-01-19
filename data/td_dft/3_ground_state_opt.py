import argparse
import os
import subprocess
from ase.io import read
from ase.calculators.gaussian import Gaussian

def run_gaussian_opt(input_xyz, out_dir, out_name):
    """
    Runs Gaussian B3LYP/6-31G* optimization on an input XYZ file.
    """
    # Ensure output directory exists
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    # Read molecule from XYZ
    mol = read(input_xyz)
    
    # Define Gaussian parameters
    kwargs = dict(
        opt='',
        chk=f"{out_name}.chk",
        basis='6-31g*',
        charge=0,
        # multiplicity=1,
        nprocshared=16,
        SCF='XQC',
        mem='60GB',
        method='b3lyp',
    )
    
    # Initialize Gaussian calculator
    gaussian = Gaussian(
        label=out_name, 
        command='g16 < PREFIX.com > PREFIX.log', 
        **kwargs
    )
    
    if 'force' in gaussian.parameters:
        del gaussian.parameters['force']
    
    print(f"Generating Gaussian input and running B3LYP optimization for {out_name} in {out_dir}...")
    
    # Change to output directory to run Gaussian
    current_dir = os.getcwd()
    os.chdir(out_dir)
    
    # Write input file
    gaussian.write_input(mol)
    
    # Run Gaussian
    try:
        cmd = f"g16 < {out_name}.com > {out_name}.log"
        subprocess.run(cmd, shell=True, check=True)
        print(f"Gaussian optimization complete. Results in {os.path.join(out_dir, out_name + '.log')} and {os.path.join(out_dir, out_name + '.chk')}")
        os.chdir(current_dir)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Gaussian failed with error: {e}")
        os.chdir(current_dir)
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        os.chdir(current_dir)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ground-state optimization using Gaussian B3LYP.")
    parser.add_argument("input", help="Input XYZ file.")
    parser.add_argument("--out_dir", default=".", help="Output directory (default: current directory).")
    parser.add_argument("--out_name", required=True, help="Output base name.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        exit(1)
        
    run_gaussian_opt(args.input, args.out_dir, args.out_name)
