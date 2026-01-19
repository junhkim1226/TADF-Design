import argparse
import os
from rdkit import Chem
from rdkit.Chem import AllChem

def smiles_to_xyz(smiles, output_filename, n_confs=50):
    """
    Converts a SMILES string to a 3D XYZ file using RDKit.
    Generates multiple conformers and selects the lowest energy one after UFF optimization.
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"Error: Could not parse SMILES '{smiles}'")
            return False
        
        mol = Chem.AddHs(mol)
        
        # Generate multiple conformers
        params = AllChem.ETKDGv3()
        params.randomSeed = 42
        conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=n_confs, params=params)
        
        if len(conf_ids) == 0:
            print("ETKDG failed, trying random coords...")
            AllChem.EmbedMolecule(mol, useRandomCoords=True)
            AllChem.UFFOptimizeMolecule(mol)
            Chem.MolToXYZFile(mol, output_filename)
            return True
        
        # Optimize each conformer and get energies
        energies = []
        for conf_id in conf_ids:
            ff = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)
            if ff is None:
                energies.append(float('inf'))
                continue
            ff.Minimize(maxIts=500)
            energies.append(ff.CalcEnergy())
        
        # Select lowest energy conformer
        best_idx = energies.index(min(energies))
        best_conf_id = conf_ids[best_idx]
        
        print(f"Generated {len(conf_ids)} conformers, best energy: {energies[best_idx]:.2f} kcal/mol")
        
        # Write best conformer to XYZ
        Chem.MolToXYZFile(mol, output_filename, confId=best_conf_id)
        print(f"Successfully created {output_filename}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SMILES to XYZ using RDKit UFF.")
    parser.add_argument("smiles", help="SMILES string of the molecule.")
    parser.add_argument("output", help="Output XYZ filename (e.g., molecule.xyz).")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    smiles_to_xyz(args.smiles, args.output)
