# Music Recommendation System
A full-stack application that predicts the popularity tier of a song based on its audio features and recommends similar songs using a hybrid filtering approach.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React.js
- **Database**: PostgreSQL
- **ML Models**: Scikit-learn (RandomForest, KNN), XGBoost
- **Data Processing**: Pandas, NumPy

## Prerequisites
- Python 3.8+
- Node.js & npm
- PostgreSQL installed and running

##  Installation & Setup

### 1. Database Setup
Ensure PostgreSQL is running and create a database named `music_db`.

```bash
createdb music_db
```

*Note: If your database credentials differ from `postgres:postgres@localhost:5432`, update `app/database.py`.*

### 2. Backend Setup
Navigate to the project root directory:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload
```

The backend will start at `http://127.0.0.1:8000`. API docs are available at `http://127.0.0.1:8000/docs`.

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory:

```bash
cd music-popularity

# Install dependencies
npm install

# Start the React app
npm start
```

The application will open at `http://localhost:3000`.

## Usage
**Song Recommendation**: 
- Enter a song name (e.g., "Dance Monkey") in the right panel.
- The system will display the **matched input song** with a Spotify player.
- It will list **5 similar songs** with their similarity scores and preview players.
- If multiple songs match the name, the system automatically selects the most popular version.

## Project Structure
- `app/`: FastAPI application code (API, Database, Schemas, Recommender Core).
- `models/`: Trained ML models (`.pkl` files).
- `notebooks/`: Jupyter notebooks and training scripts (`train.py`).
- `music-popularity/`: React frontend source code.
- `data/`: Dataset files.
