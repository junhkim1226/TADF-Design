import argparse
import os
import subprocess

ORCA_PATH = "/appl/orca_4.2.1/orca_4_2_1_linux_x86-64_openmpi314/orca"

def run_orca_xtb(input_xyz, out_dir, out_name):
    """
    Runs ORCA GFN-xtB2 optimization on an input XYZ file.
    """
    # Ensure output directory exists
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # Define paths
    input_file = os.path.join(out_dir, f"{out_name}.inp")
    log_file = os.path.join(out_dir, f"{out_name}.out")
    
    # Read coordinates from XYZ file
    with open(input_xyz, 'r') as f:
        xyz_lines = f.readlines()
    
    # Extract atom count and coordinates (skipping the first two lines of XYZ)
    coords = "".join(xyz_lines[2:])
    
    # Create ORCA input file
    orca_input = f"""! XTB2 Opt
* xyz 0 1
{coords}*
"""
    with open(input_file, 'w') as f:
        f.write(orca_input)
    
    print(f"Running ORCA GFN-xtB2 optimization for {out_name} in {out_dir}...")
    try:
        # Run ORCA
        # ORCA creates many temporary files, so it's better to run it in the output directory
        current_dir = os.getcwd()
        os.chdir(out_dir)
        
        # We need to use the absolute path for ORCA and the relative path for the input file
        # Since we chdir to out_dir, the input file is just out_name.inp
        with open(f"{out_name}.out", 'w') as out:
            subprocess.run([ORCA_PATH, f"{out_name}.inp"], stdout=out, stderr=subprocess.STDOUT, check=True)
        
        os.chdir(current_dir)
        
        # Check if optimization finished and extract the new XYZ
        # ORCA saves the optimized coordinates in {out_name}.xyz in the directory it was run
        optimized_xyz = os.path.join(out_dir, f"{out_name}.xyz")
        if os.path.exists(optimized_xyz):
            print(f"Optimization complete. Optimized coordinates saved to {optimized_xyz}")
            return True
        else:
            print(f"Error: Optimized XYZ file {optimized_xyz} not found.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"ORCA failed with error: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-optimize XYZ using ORCA GFN-xtB2.")
    parser.add_argument("input", help="Input XYZ file.")
    parser.add_argument("--out_dir", default=".", help="Output directory (default: current directory).")
    parser.add_argument("--out_name", required=True, help="Output base name (e.g., molecule_opt).")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        exit(1)
        
    run_orca_xtb(args.input, args.out_dir, args.out_name)
