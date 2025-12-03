import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import joblib
import os
import sys


sys.path.append(os.getcwd())
try:
    from app.recommender_core import MusicRecommender
except ImportError:
    print("Error: Cannot find app.recommender_core. Please run this script from the project root.")
    sys.exit(1)


print("Starting model training")


# path settings
DATA_PATH = 'data/spotify_songs.csv'
MODELS_DIR = 'models'

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

# load data
if not os.path.exists(DATA_PATH):
    print(f" Error: {DATA_PATH} not found.")
    sys.exit(1)

df = pd.read_csv(DATA_PATH).dropna()

# feature engineering
print("Feature Engineering...")
# popularity tier (used for display/filtering)
df['popularity_tier'], bin_edges = pd.qcut(df['track_popularity'], q=5, labels=[0, 1, 2, 3, 4], retbins=True)
# time features
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'], errors='coerce')
df['track_age'] = 2025 - df['track_album_release_date'].dt.year.fillna(2020)
# one-hot
df_encoded = pd.get_dummies(df, columns=['playlist_genre', 'playlist_subgenre'], drop_first=True)





print("Building Recommendation System...")

# prepare recommendation data (full dataset)
recommendation_data = df_encoded.copy()
# Add back the original genre column for display
recommendation_data['playlist_genre'] = df['playlist_genre']

# Feature List
audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode',
                  'speechiness', 'acousticness', 'instrumentalness',
                  'liveness', 'valence', 'tempo', 'duration_ms']
genre_cols = [col for col in df_encoded.columns if 'playlist_genre_' in col or 'playlist_subgenre_' in col]
rec_features = audio_features + genre_cols

# train knn
scaler = StandardScaler()
X_rec = recommendation_data[rec_features]
X_rec_scaled = scaler.fit_transform(X_rec)

knn_model = NearestNeighbors(n_neighbors=20, metric='cosine', algorithm='brute', n_jobs=-1)
knn_model.fit(X_rec_scaled)

# encapsulate object (using class from app.recommender_core)
# this ensures pickle saves the class path as app.recommender_core.MusicRecommender
# so FastAPI can load it correctly
recommender = MusicRecommender(
    knn_model=knn_model,
    scaler=scaler,
    song_data=recommendation_data,
    features=rec_features
)

print("Recommendation Model Encapsulated!")

# Save recommendation model
joblib.dump(recommender, os.path.join(MODELS_DIR, 'music_recommender.pkl'))

# Save auxiliary files
joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
recommendation_data.to_csv(os.path.join(MODELS_DIR, '../data/processed_songs.csv'), index=False)

print("All models retrained and saved locally!")
