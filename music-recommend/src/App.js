// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // --- State Management ---
  const [recommendations, setRecommendations] = useState([]);
  const [matchedSong, setMatchedSong] = useState(null);


  // Recommendation Search Term
  const [searchSong, setSearchSong] = useState("");

  // --- API Calls ---

  const handleRecommend = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/recommend/song/${searchSong}`);
      setRecommendations(response.data.results); 
      // 复用 predictionResult 状态来存 input_song，或者新建一个状态。
      // 为了简单，这里我们新建一个临时对象存到 predictionResult 里，或者新建一个专门的 state
      // 更好的做法是新建 state，但为了少改代码，我这里把 input_song 塞到 predictionResult 里 (如果它为空的话)
      // 或者更规范一点：
      setMatchedSong(response.data.input_song);
    } catch (error) {
      alert("Song not found or backend error.");
    }
  };



  return (
    <div className="container">
      <div className="header">
        <h1>🎵 Music Analytics Platform</h1>
        <p>Powered by React & FastAPI</p>
      </div>

      <div className="grid">
        {/* Recommender Card */}
        <div className="card" style={{ gridColumn: '1 / -1', maxWidth: '800px', margin: '0 auto' }}>
          <h2>🎧 Song Recommender</h2>
          <div className="form-group">
            <label>Enter a Song Name</label>
            <input 
              placeholder="e.g. Dance Monkey" 
              value={searchSong} 
              onChange={(e) => setSearchSong(e.target.value)}
            />
          </div>
          <button className="btn" style={{backgroundColor: '#9b59b6'}} onClick={handleRecommend}>
            Find Similar Songs
          </button>

          {recommendations.length > 0 && (
            <div className="result-box" style={{borderLeftColor: '#9b59b6'}}>
              {/* 新增：显示输入歌曲（匹配到的） */}
              {matchedSong && (
                <div style={{marginBottom: '20px', paddingBottom: '15px', borderBottom: '1px dashed #ccc'}}>
                  <h4>🎯 Matched Song:</h4>
                  <div className="song-item" style={{flexDirection: 'column', border: 'none', padding: 0}}>
                    <div style={{marginBottom: '5px'}}>
                      <strong>{matchedSong.track_name}</strong>
                      <span style={{color: '#666', fontSize: '0.9em'}}> by {matchedSong.track_artist}</span>
                    </div>
                    <iframe 
                      style={{borderRadius: '12px'}} 
                      src={`https://open.spotify.com/embed/track/${matchedSong.track_id}?utm_source=generator`} 
                      width="100%" 
                      height="80" 
                      frameBorder="0" 
                      allowFullScreen="" 
                      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                      loading="lazy"
                      title="Input Song Player"
                    ></iframe>
                  </div>
                </div>
              )}

              <h3>Recommended Songs</h3>
              {recommendations.map((song, idx) => (
                    <div key={idx} className="song-item">
                      
                      {/* Song Info Row */}
                      <div className="song-info">
                        <div>
                          <div className="song-title">{song.track_name}</div>
                          <div className="song-artist">
                            {song.track_artist}
                            <span className="song-meta">{song.genre}</span>
                          </div>
                        </div>
                        <div className="song-score">{(song.similarity * 100).toFixed(0)}% Match</div>
                      </div>

                      {/* Spotify Player */}
                      <div style={{width: '100%'}}>
                        <iframe 
                          style={{borderRadius: '12px'}} 
                          src={`https://open.spotify.com/embed/track/${song.track_id}?utm_source=generator`} 
                          width="100%" 
                          height="80" 
                          frameBorder="0" 
                          allowFullScreen="" 
                          allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                          loading="lazy"
                          title={`Spotify Player ${idx}`}
                        ></iframe>
                      </div>

                    </div>
                  ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;