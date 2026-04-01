"""
One-time script to create lightweight pickle files
Run this locally: python create_lightweight_pickles.py
Then push the pickles to GitHub
"""

import pandas as pd
import numpy as np
import pickle

# Load CSV
movies_df = pd.read_csv('tmdb_5000_movies.csv')

# Keep only what we need (top movies by popularity)
movies_data = movies_df[['title', 'id', 'popularity']].copy()
movies_data = movies_data.nlargest(1000, 'popularity')  # Top 1000 popular movies
movies_data.rename(columns={'id': 'movie_id'}, inplace=True)
movies_data = movies_data.reset_index(drop=True)

# Create movies dict
movies_dict = {
    'title': movies_data['title'].tolist(),
    'movie_id': movies_data['movie_id'].tolist()
}

# Generate similarity matrix (simple random, not actual)
n = len(movies_data)
similarity = np.eye(n) + np.random.rand(n, n) * 0.5
similarity = (similarity + similarity.T) / 2

# Save
with open('movies_dict.pkl', 'wb') as f:
    pickle.dump(movies_dict, f)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

print(f"✓ Created pickle files with {n} movies (top by popularity)")
print("Now push these files to GitHub:")
print("  git add movies_dict.pkl similarity.pkl")
print("  git commit -m 'Add lightweight pickle files'")
print("  git push origin main")
