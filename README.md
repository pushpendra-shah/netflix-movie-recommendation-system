# Netflix Movie Recommendation System

A movie recommendation web app I built using FastAPI. You type in a movie name and it shows you similar movies based on things like genre, cast, director and the plot.

I went with a content-based approach for this. The idea is pretty simple: I convert each movie's details into numbers using TF-IDF, and then use cosine similarity to find which movies are closest to the one you searched for. I also added fuzzy matching with difflib, so even if you type the movie name a little wrong, it still finds the right one.

# What it does
- Suggests similar movies for whatever title you search
- Still works if you misspell the movie name
- Uses TF-IDF and cosine similarity on the movie data
- Saves the processed data with pickle so it responds quickly
- Backend is built with FastAPI

# Tech I used
Python, FastAPI, Uvicorn, scikit-learn, Pandas, difflib, pickle

# How to run it

Clone the repo:
```bash
git clone https://github.com/pushpendra-shah/netflix-movie-recommendation-system.git
cd netflix-movie-recommendation-system
```

Install the libraries:
```bash
pip install fastapi uvicorn scikit-learn pandas
```

Run it:
```bash
uvicorn main:app --reload
```

Then open http://localhost:8000 in your browser.

# Files in this project
- main.py - the FastAPI app and the recommendation logic
- index.html - the frontend page
- movie_dict.pkl - the saved movie data

# Things I want to add later
- Recommendations based on user ratings (collaborative filtering)
- Movie posters using a public movie API
- Deploy it online so there's a live demo link
