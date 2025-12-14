"""
Example Python script for debugging in VS Code/Cursor

This demonstrates how to use debugging features:
1. Set breakpoints by clicking left of line numbers
2. Press F5 to start debugging
3. Use Debug Console to inspect variables
4. Use Step Over (F10), Step Into (F11), Step Out (Shift+F11)
"""

import pandas as pd
import numpy as np

def load_and_process_data():
    """Example function to demonstrate debugging"""
    # Set a breakpoint on the next line by clicking left of line number
    base_path = '/Users/winstonfeng/Downloads/Rilla/Rilla data'
    
    # Load a small dataset
    print("Loading manager_data...")
    manager_data = pd.read_csv(f'{base_path}/manager_data.csv')
    
    # Set another breakpoint here to inspect manager_data
    print(f"Loaded {len(manager_data)} rows")
    
    # Process data
    result = process_columns(manager_data)
    
    return result

def process_columns(df):
    """Another function to step into"""
    # You can step into this function using F11
    column_count = len(df.columns)
    row_count = len(df)
    
    # Inspect these variables in the Debug Console
    print(f"DataFrame shape: {row_count} rows × {column_count} columns")
    
    # Example: check for missing values
    missing_values = df.isnull().sum()
    
    return {
        'columns': column_count,
        'rows': row_count,
        'missing': missing_values.sum()
    }

if __name__ == "__main__":
    # Main entry point - set breakpoint here
    print("Starting data processing...")
    
    # Step through this function call
    result = load_and_process_data()
    
    # Final breakpoint to inspect results
    print("Processing complete!")
    print(f"Result: {result}")



