import os
import pandas as pd

def get_dataset_path():
    """Return the path to the local data directory."""
    base_path = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_path, 'data')
    print(f"Using local dataset at: {data_path}")
    return data_path

def find_data_file(base_path):
    """Find the train parquet file directly."""
    print("Searching in directory:", base_path)
    
    target_file = os.path.join(base_path, "train_ember_2018_v2_features.parquet")
    
    if os.path.exists(target_file):
        print("File found successfully!")
        return target_file
    else:
        print("Error: Train file not found. Directory contents:")
        print(os.listdir(base_path))
        return None

def load_subset(file_path, max_rows=10000):
    """Load the first 10,000 rows from the parquet file."""
    if not file_path:
        return []
        
    print(f"Loading first {max_rows} rows from parquet file (this might take a moment)...")
    try:
        # Read the parquet file
        df = pd.read_parquet(file_path)
        
        # Keep only the first max_rows to save RAM
        df_subset = df.head(max_rows)
        
        # Convert to a list of dictionaries
        records = df_subset.to_dict('records')
        print(f"Successfully loaded {len(records)} records.")
        return records
    except Exception as e:
        print(f"Error reading parquet file: {e}")
        return []