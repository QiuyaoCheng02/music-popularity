# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional



# Recommendation Output Model
class SongItem(BaseModel):
    track_name: str
    track_artist: str
    genre: str
    similarity: float
    track_popularity: int
    track_id: str

class RecommendationOutput(BaseModel):
    query: str
    input_song: Optional[SongItem] = None
    results: List[SongItem]