# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np
import os
import sys

# Add current directory to path to ensure recommender_core is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from . import database, schemas, crud, recommender_core

# 1. Initialize App
app = FastAPI(
    title="Music Analytics Platform API",
    description="Backend for Popularity Prediction & Music Recommendation",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to ["http://localhost:3000"] for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],
)

# Try to connect to database
database.init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. Global Variables & Model Loading
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

models = {}

@app.on_event("startup")
def load_models():
    print("⏳ Loading AI Models...")
    try:
        # Load full recommender system object
        # Note: recommender_core.MusicRecommender class definition must exist
        models['recommender'] = joblib.load(os.path.join(MODEL_DIR, "music_recommender.pkl"))
        
        print("✅ All Models Loaded Successfully!")
    except FileNotFoundError as e:
        print(f"❌ Error: Model file not found. Check {MODEL_DIR}. Details: {e}")
    except Exception as e:
        print(f"❌ Error loading models: {e}")

# 3. Root Path
@app.get("/")
def read_root():
    return {"status": "running", "docs_url": "/docs"}



# 4. Recommendation Endpoint (By Song Name)
@app.get("/recommend/song/{song_name}", response_model=schemas.RecommendationOutput)
def recommend_by_name(song_name: str):
    if 'recommender' not in models:
        raise HTTPException(status_code=500, detail="Recommender model not loaded")
    
    rec_engine = models['recommender']
    
    # Call method defined in recommender_core
    input_details, result = rec_engine.recommend_by_song_name(song_name, n_recommendations=5)
    
    if input_details is None: # If not found
        raise HTTPException(status_code=404, detail=result)
        
    # Format output
    output_list = []
    for _, row in result.iterrows():
        output_list.append({
            "track_name": row['track_name'],
            "track_artist": row['track_artist'],
            "genre": row['genre'] if 'genre' in row else "Unknown",
            "similarity": float(row['similarity']),
            "track_popularity": int(row['track_popularity']),
            "track_id": row['track_id']
        })
        
    return {
        "query": song_name,
        "input_song": input_details,
        "results": output_list
    }

# 5. Recommendation Endpoint (By Features - Advanced)
@app.post("/recommend/features", response_model=schemas.RecommendationOutput)
def recommend_by_features(features: dict):
    if 'recommender' not in models:
        raise HTTPException(status_code=500, detail="Recommender model not loaded")
    
    rec_engine = models['recommender']
    
    try:
        # Call feature recommendation method
        result = rec_engine.recommend_by_features(features, n_recommendations=5)
        
        output_list = []
        for _, row in result.iterrows():
            output_list.append({
                "track_name": row['track_name'],
                "track_artist": row['track_artist'],
                "genre": row['genre'] if 'genre' in row else "Unknown",
                "similarity": float(row['similarity']),
                "track_popularity": int(row['track_popularity']),
                "track_id": row['track_id']
            })
            
        return {
            "query": "Custom Features",
            "results": output_list
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))