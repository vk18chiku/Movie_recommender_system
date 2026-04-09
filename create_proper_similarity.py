"""
Create proper similarity matrix from movie genres and keywords
This generates accurate recommendations based on movie features
"""

import pandas as pd
import numpy as np
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_movie_features(row):
    """Combine genres and keywords into a feature string"""
    features = []
    
    # Add genres
    try:
        if isinstance(row['genres'], str):
            genres = json.loads(row['genres'].replace("'", '"'))
            features.extend([g['name'] for g in genres])
    except:
        pass
    
    # Add keywords
    try:
        if isinstance(row['keywords'], str):
            keywords = json.loads(row['keywords'].replace("'", '"'))
            features.extend([k['name'] for k in keywords[:5]])  # Top 5 keywords
    except:
        pass
    
    return ' '.join(features) if features else 'unknown'

print("Loading data...")
movies_df = pd.read_csv('tmdb_5000_movies.csv')
credits_df = pd.read_csv('tmdb_5000_credits.csv')

# Merge
movies = movies_df.merge(credits_df, on='title')

# Get features
print("Extracting features...")
movies['features'] = movies.apply(get_movie_features, axis=1)

# Compute TF-IDF
print("Computing TF-IDF...")
tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['features'])

# Compute similarity
print("Computing similarity matrix (this may take a minute)...")
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create movies dict
print("Saving pickle files...")
movies_dict = {
    'title': movies['title'].tolist(),
    'movie_id': movies['id'].tolist()
}

# Save
with open('movies_dict.pkl', 'wb') as f:
    pickle.dump(movies_dict, f)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity_matrix, f)

print(f"✓ Created pickle files with {len(movies)} movies")
print(f"✓ Similarity matrix shape: {similarity_matrix.shape}")
print("\nNow push to GitHub:")
print("  git add movies_dict.pkl similarity.pkl")
print("  git commit -m 'Add proper similarity matrix for all 5000 movies'")
print("  git push origin main")
