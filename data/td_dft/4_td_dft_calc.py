import argparse
import os
import subprocess

def run_gaussian_td(input_chk, out_dir, out_name):
    """
    Runs Gaussian TD-DFT (B3LYP/6-31G*) on an input CHK file.
    """
    # Ensure output directory exists
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    input_com = os.path.join(out_dir, f"{out_name}.com")
    input_log = os.path.join(out_dir, f"{out_name}.log")
    
    # Get absolute path for input_chk because we might change directory
    abs_chk_path = os.path.abspath(input_chk)
    
    # Define Gaussian input content for TD-DFT
    orca_input = f"""%OldChk={abs_chk_path}
%nprocshared=16
%mem=60GB
# b3lyp/6-31g* TD=(Nstates=1,50-50) Geom=Check Guess=Read SCF=XQC

TD-DFT calculation

0 1

"""
    with open(input_com, 'w') as f:
        f.write(orca_input)
    
    print(f"Generating Gaussian TD-DFT input and running calculation for {out_name} in {out_dir}...")
    
    # Run Gaussian
    try:
        current_dir = os.getcwd()
        os.chdir(out_dir)
        cmd = f"g16 < {out_name}.com > {out_name}.log"
        subprocess.run(cmd, shell=True, check=True)
        os.chdir(current_dir)
        print(f"Gaussian TD-DFT calculation complete. Results in {input_log}")
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
    parser = argparse.ArgumentParser(description="TD-DFT calculation using Gaussian.")
    parser.add_argument("input", help="Input CHK file.")
    parser.add_argument("--out_dir", default=".", help="Output directory (default: current directory).")
    parser.add_argument("--out_name", required=True, help="Output base name.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input CHK file {args.input} not found.")
        exit(1)
        
    run_gaussian_td(args.input, args.out_dir, args.out_name)
