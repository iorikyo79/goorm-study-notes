import pandas as pd
import os

# Paths
DATA_PATH = "data/ALL.csv"
ABBREVIATION_COL = "Abbreviation"
MEANING_COL = "Meaning"

def load_kb(path):
    """Loads the CSV and returns a dictionary of Abbreviation -> List of Meanings."""
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return {}
    
    try:
        df = pd.read_csv(path)
        # Clean data: drop rows with NaN in Abbreviation
        df = df.dropna(subset=[ABBREVIATION_COL])
        
        kb = {}
        for index, row in df.iterrows():
            abbr = str(row[ABBREVIATION_COL]).strip().upper() # Normalize to uppercase
            meaning = str(row[MEANING_COL]).strip()
            
            if abbr not in kb:
                kb[abbr] = []
            kb[abbr].append(meaning)
            
        print(f"Loaded {len(kb)} unique abbreviations from {path}.")
        return kb
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return {}

def run_experiment(kb):
    """Tests the KB against known FPs and TPs."""
    
    # Target False Positives (should be in KB as medical abbreviations)
    target_fps = ["TAH", "RSO", "SMA"]
    
    # Target True Positives (should NOT be in KB, or handled)
    # "Samsung Medical Center" is a hospital name, not a general medical condition/procedure abbreviation.
    # It might appear if the list is very broad, but ideally it shouldn't be confused with a condition.
    target_tps = ["Samsung Medical Center", "SAMSUNG MEDICAL CENTER"] 

    print("\n--- Experiment Results ---")
    
    # Check FPs
    print("\nChecking for potential False Positives (Should be in KB):")
    for abbr in target_fps:
        if abbr in kb:
            print(f"[FOUND] {abbr}: {kb[abbr]}")
        else:
            print(f"[MISSING] {abbr} not found in KB.")

    # Check TPs
    print("\nChecking for potential True Positives (Should NOT be in KB):")
    for term in target_tps:
        normalized_term = term.upper()
        if normalized_term in kb:
            print(f"[WARNING] {term} found in KB as: {kb[normalized_term]}")
        else:
            print(f"[PASS] {term} not found in KB.")

if __name__ == "__main__":
    print("Starting FP Hunter v2 Experiment...")
    kb = load_kb(DATA_PATH)
    if kb:
        run_experiment(kb)
