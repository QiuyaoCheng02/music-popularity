# app/recommender_core.py
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

class MusicRecommender:
    def __init__(self, knn_model, scaler, song_data, features):
        self.knn_model = knn_model
        self.scaler = scaler
        self.song_data = song_data  # Contains song name, artist, etc.
        self.features = features
        # Note: Assumes data passed during initialization is already a DataFrame
        # If loading object fails, it might be because feature_matrix was included in save
        # Just ensure method names and attributes match
        if hasattr(scaler, 'transform') and not song_data.empty:
             self.feature_matrix = scaler.transform(song_data[features])
        
    def recommend_by_song_name(self, song_name, n_recommendations=10):
        """Recommend similar songs based on song name"""
        # Find song
        matches = self.song_data[self.song_data['track_name'].str.contains(song_name, case=False, na=False)]
        
        if len(matches) == 0:
            return None, f"❌ Song not found: {song_name}"
        
        # Fallback: If multiple matches, sort by popularity and take the most popular one
        matches = matches.sort_values('track_popularity', ascending=False)
        song_idx = matches.index[0]
        
        # Extract input song details
        input_song_details = {
            'track_name': self.song_data.loc[song_idx, 'track_name'],
            'track_artist': self.song_data.loc[song_idx, 'track_artist'],
            'track_popularity': int(self.song_data.loc[song_idx, 'track_popularity']),
            'genre': self.song_data.loc[song_idx, 'playlist_genre'] if 'playlist_genre' in self.song_data.columns else "Unknown",
            'track_id': self.song_data.loc[song_idx, 'track_id'],
            'similarity': 1.0
        }
        
        return input_song_details, self.recommend_by_index(song_idx, n_recommendations)
    
    def recommend_by_index(self, song_idx, n_recommendations=10):
        """Recommend similar songs based on index"""
        # Get song features
        # Note: self.feature_matrix must be generated before object is pickled
        song_features = self.feature_matrix[song_idx].reshape(1, -1)
        
        # Find most similar songs (get more candidates to allow for filtering)
        distances, indices = self.knn_model.kneighbors(song_features, n_neighbors=n_recommendations + 10)
        
        indices = indices[0]
        distances = distances[0]
        
        # Get input song details for filtering
        input_track_name = self.song_data.loc[song_idx, 'track_name']
        input_track_artist = self.song_data.loc[song_idx, 'track_artist']
        
        # Build recommendation results
        recommendations = []
        for idx, dist in zip(indices, distances):
            # Skip if it's the same song (same name and artist)
            current_name = self.song_data.loc[idx, 'track_name']
            current_artist = self.song_data.loc[idx, 'track_artist']
            
            if current_name == input_track_name and current_artist == input_track_artist:
                continue
                
            recommendations.append({
                'track_name': current_name,
                'track_artist': current_artist,
                'similarity': 1 - dist,  # Convert to similarity
                'track_popularity': int(self.song_data.loc[idx, 'track_popularity']), # Convert to int for JSON serialization
                'genre': self.song_data.loc[idx, 'playlist_genre'] if 'playlist_genre' in self.song_data.columns else "Unknown",
                'track_id': self.song_data.loc[idx, 'track_id']
            })
            
            if len(recommendations) >= n_recommendations:
                break
        
        return pd.DataFrame(recommendations)
    
    def recommend_by_features(self, feature_dict, n_recommendations=10):
        """Recommend songs based on feature values"""
        # Build feature vector
        feature_vector = pd.DataFrame([feature_dict])[self.features]
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Find most similar songs
        distances, indices = self.knn_model.kneighbors(feature_vector_scaled, n_neighbors=n_recommendations)
        
        indices = indices[0]
        distances = distances[0]
        
        # Build recommendation results
        recommendations = []
        for idx, dist in zip(indices, distances):
            recommendations.append({
                'track_name': self.song_data.loc[idx, 'track_name'],
                'track_artist': self.song_data.loc[idx, 'track_artist'],
                'similarity': 1 - dist,
                'track_popularity': int(self.song_data.loc[idx, 'track_popularity']),
                'genre': self.song_data.loc[idx, 'playlist_genre'] if 'playlist_genre' in self.song_data.columns else "Unknown",
                'track_id': self.song_data.loc[idx, 'track_id'] 
            })
        return pd.DataFrame(recommendations)