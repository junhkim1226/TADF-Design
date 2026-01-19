#!/usr/bin/env python
"""Validate TD-DFT results against reference CSV data."""
import pandas as pd
import re
from pathlib import Path

CSV_PATH = "./test_data.csv"
RESULTS_DIR = Path("./example_logs")

def parse_td_log(log_path):
    """Extract S1 and T1 energies (eV) from td.log."""
    s1, t1 = None, None
    with open(log_path) as f:
        for line in f:
            if "Excited State" in line:
                match = re.search(r"(Singlet|Triplet)-\w+\s+([\d.]+)\s+eV", line)
                if match:
                    state_type, energy = match.groups()
                    if state_type == "Triplet" and t1 is None:
                        t1 = float(energy)
                    elif state_type == "Singlet" and s1 is None:
                        s1 = float(energy)
                if s1 and t1:
                    break
    return s1, t1

def main():
    df = pd.read_csv(CSV_PATH)
    ref = {f"mol_{r['MolID']}": (r['S1'], r['T1']) for _, r in df.iterrows()}
    
    print(f"{'MolID':<12} {'S1_ref':>8} {'S1_calc':>8} {'T1_ref':>8} {'T1_calc':>8} {'ΔS1':>8} {'ΔT1':>8}")
    print("-" * 72)
    
    for mol_dir in sorted(RESULTS_DIR.glob("mol_*")):
        mol_id = mol_dir.name
        log_path = mol_dir / "td.log"
        
        if not log_path.exists():
            print(f"{mol_id:<12} -- log not found --")
            continue
        
        s1_calc, t1_calc = parse_td_log(log_path)
        s1_ref, t1_ref = ref.get(mol_id, (None, None))
        
        ds1 = f"{s1_calc - s1_ref:.4f}" if s1_calc and s1_ref else "N/A"
        dt1 = f"{t1_calc - t1_ref:.4f}" if t1_calc and t1_ref else "N/A"
        
        print(f"{mol_id:<12} {s1_ref or 'N/A':>8} {s1_calc or 'N/A':>8} "
              f"{t1_ref or 'N/A':>8} {t1_calc or 'N/A':>8} {ds1:>8} {dt1:>8}")

if __name__ == "__main__":
    main()
