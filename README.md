# Movie Recommender System

A machine learning-powered web application that recommends movies based on user selection using collaborative filtering and content-based recommendations.

## Features

- **Movie Search & Selection**: Browse and select from 5000+ movies
- **Smart Recommendations**: Get 5 personalized movie recommendations
- **Movie Posters**: Display poster images for recommended movies using TMDB API
- **Robust Error Handling**: Retry logic and caching for API calls
- **Fast & Responsive**: Built with Streamlit for instant UI updates

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data**: Pandas, NumPy
- **APIs**: TMDB (The Movie Database)
- **ML**: Similarity-based recommendations using pickle-serialized models

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/vk18chiku/Movie_recommender_system.git
cd Movie_recommender_system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application locally**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
Movie_recommender_system/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── movies_dict.pkl            # Serialized movies dictionary
├── similarity.pkl             # Pre-computed similarity matrix
├── tmdb_5000_movies.csv       # Movie dataset
├── tmdb_5000_credits.csv      # Credits dataset
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── README.md                  # This file
```

## How It Works

1. **Load Data**: The system loads pre-processed movies data and similarity matrix from pickle files
2. **User Selection**: User selects a movie from the dropdown
3. **Find Similar Movies**: Uses cosine similarity to find the 5 most similar movies
4. **Fetch Posters**: Retrieves movie posters from TMDB API with retry logic
5. **Display Results**: Shows recommended movies with their posters in a 5-column layout

## Feature Engineering Pipeline

The recommendation system uses advanced feature engineering to create rich movie representations:

### 1. **Data Integration**
- Merged TMDB movies and credits datasets on movie title
- Selected relevant features: genres, keywords, cast, crew, overview

### 2. **JSON Data Extraction**
- **Genres**: Extracted genre names from JSON format
- **Keywords**: Extracted movie keywords from JSON format
- **Cast**: Extracted top 3 actor names from cast list
- **Crew**: Extracted director names from crew information

### 3. **Text Preprocessing**
- Removed null values from dataset
- Split movie overviews into individual words
- Removed spaces from genre, keywords, cast, and crew names for better matching

### 4. **Feature Combination**
- Created composite "tags" feature by concatenating:
  - All genres
  - All keywords
  - Top 3 cast members
  - Director name
  - Movie overview text

### 5. **Text Normalization**
- Converted all tags to lowercase for consistency
- Applied **Porter Stemming** to reduce words to their root form
  - Example: "running", "runs", "ran" all become "run"

### 6. **Vectorization**
- Used **CountVectorizer** from scikit-learn
- Extracted 5000 most frequent features
- Removed common English stop words (the, a, an, etc.)
- Converted text tags into numerical vectors

### 7. **Similarity Matrix Computation**
- Computed **Cosine Similarity** between all movie vectors
- Created a 5000×5000 similarity matrix
- Similarity ranges from 0 (no match) to 1 (identical)

### 8. **Model Persistence**
- Saved processed data as `movies_dict.pkl`
- Saved similarity matrix as `similarity.pkl`
- Enables fast loading without recomputation

### Result
The feature engineering pipeline transforms raw movie metadata into a semantic representation that captures:
- Thematic elements (genres, keywords)
- Creative team (cast, director)
- Plot context (overview)

This enables the system to find movies with similar themes, actors, and storytelling styles.

## API Integration

The app uses the **TMDB API** to fetch movie posters. The API key is included in the code for demonstration purposes.

**Note**: For production deployment, consider moving the API key to environment variables.

## Deployment

### Live Application

The application is deployed and live at: **[https://movie-recommender-system-3-1pxt.onrender.com/](https://movie-recommender-system-3-1pxt.onrender.com/)**

### Deploy on Render (Recommended for Streamlit)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `streamlit run app.py`
7. Deploy!

**Free tier includes**:
- Automatic deployments from GitHub
- 750 hours/month runtime
- Sleeps after 15 mins of inactivity

## Requirements

```
streamlit==1.28.1
pandas==1.5.3
numpy==1.24.4
requests==2.31.0
urllib3==2.0.7
```

## Usage

1. Select a movie from the dropdown (type to search)
2. Click the **"Show Recommendation"** button
3. View 5 recommended movies with their posters

## Features Explained

### Retry Logic
- Handles API rate limiting automatically
- Exponential backoff for failed requests
- Graceful fallback to placeholder images

### Caching
- Stores fetched posters in memory
- Reduces API calls for repeated movie selections
- Faster response times

### Error Handling
- Handles missing posters elegantly
- Shows error messages for failed recommendations
- Continues functioning even if API is temporarily down

## Future Enhancements

- [ ] Add more recommendation algorithms (collaborative filtering, matrix factorization)
- [ ] Include user ratings and reviews
- [ ] Add filtering by genre, year, and rating
- [ ] Implement user accounts for personalized recommendations
- [ ] Add watchlist functionality
- [ ] Integrate with streaming platforms

## Dataset Information

- **Movies**: 5000 movies from TMDB
- **Features**: Title, genres, keywords, cast, crew, ratings, and more
- **Source**: [Kaggle TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, feel free to reach out or open an issue on GitHub.

---

**Happy movie watching! 🎬🍿**
