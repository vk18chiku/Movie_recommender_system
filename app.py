import pickle
import streamlit as st
import numpy as np
import pandas as pd
import requests
import time
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Cache for poster URLs
poster_cache = {}

def create_default_data_if_missing():
    """Load pickle files - they should exist in repo"""
    if not os.path.exists('movies_dict.pkl') or not os.path.exists('similarity.pkl'):
        raise FileNotFoundError("Pickle files not found! Add movies_dict.pkl and similarity.pkl to repo")
    return True

def create_session_with_retries():
    """Create requests session with aggressive retry strategy"""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=(500, 502, 504, 429),
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def fetch_poster(movie_id):
    """Fetch poster from TMDB API with error handling and caching"""
    # Check cache first
    if movie_id in poster_cache:
        return poster_cache[movie_id]
    
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        session = create_session_with_retries()
        # Add delay to avoid rate limiting
        time.sleep(0.5)
        
        data = session.get(url, timeout=15, headers=headers)
        data.raise_for_status()
        data = data.json()
        
        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            poster_cache[movie_id] = full_path
            return full_path
        else:
            placeholder = "https://via.placeholder.com/500x750?text=No+Poster"
            poster_cache[movie_id] = placeholder
            return placeholder
            
    except Exception as e:
        placeholder = "https://via.placeholder.com/500x750?text=Connection+Error"
        poster_cache[movie_id] = placeholder
        return placeholder

def recommend(movie):
    """Get recommended movies"""
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return [], []

st.header('Movie Recommender System')

# Create default data if missing (for Render deployment)
create_default_data_if_missing()

# Load the data
try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    with st.spinner('Loading recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    if recommended_movie_names:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
    else:
        st.error("Could not get recommendations. Please try again.")



