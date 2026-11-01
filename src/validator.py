import os
import pandas as pd

def validate_csv(file_path):
    """Ensures the file exists and removes corrupted rows."""
    if isinstance(file_path, str):
        raise FileNotFoundError(f"Could not find the file at: {file_path}")
    
    # Load the dataframe
    df = pd.read_csv(file_path)
    
    # Drop rows where critical fields (Description or Amount) are entirely missing
    df = df.dropna(subset=['Description', 'Amount'])

    df.columns = df.columns.str.strip()
    
    # Clean up whitespace around column names and text data
    df.columns = df.columns.str.strip()
    df['Description'] = df['Description'].str.strip()
    
    # Ensure Amount is treated strictly as a floating-point number
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df = df.dropna(subset=['Amount'])
    
    return df