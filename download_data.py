"""
Download required data files from Kaggle or alternative source
Run this before starting the app if pickle files are missing
"""

import os
import pickle
import pandas as pd
import numpy as np

def check_files():
    """Check if required pickle files exist"""
    return os.path.exists('movies_dict.pkl') and os.path.exists('similarity.pkl')

def create_dummy_data():
    """Create dummy data files if they don't exist (for testing on Render)"""
    if check_files():
        return True
    
    print("Creating dummy data files...")
    
    try:
        # Create a dummy movies dict
        movies_dict = {
            'title': ['Movie 1', 'Movie 2', 'Movie 3'],
            'movie_id': [1, 2, 3]
        }
        
        # Create a dummy similarity matrix
        similarity = np.array([
            [1.0, 0.5, 0.3],
            [0.5, 1.0, 0.4],
            [0.3, 0.4, 1.0]
        ])
        
        # Save pickle files
        with open('movies_dict.pkl', 'wb') as f:
            pickle.dump(movies_dict, f)
        
        with open('similarity.pkl', 'wb') as f:
            pickle.dump(similarity, f)
        
        print("✓ Dummy data files created")
        return True
    except Exception as e:
        print(f"Error creating data files: {e}")
        return False

if __name__ == "__main__":
    if not check_files():
        create_dummy_data()
    else:
        print("Data files already exist")
