from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import pickle
import pandas as pd
import difflib

app = FastAPI()

templates = Jinja2Templates(directory=".")

movies = None
similarity = None
list_of_all_titles = []

try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    list_of_all_titles = movies['title'].tolist()
    print("AI Model and Netflix Database loaded successfully!")
except Exception as e:
    print(f"Model files load nahi hui (Error: {e}). Fallback dummy database chalega.")

MOCK_DATABASE = {
    "inception": ["Interstellar", "The Prestige", "Memento", "The Dark Knight", "Shutter Island"],
    "avatar": ["Guardians of the Galaxy", "Aliens", "Star Wars", "The Martian", "Interstellar"],
    "toy story": ["Finding Nemo", "Monsters, Inc.", "Cars", "Up", "A Bug's Life"]
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, name="index.html")

@app.get("/recommend")
async def recommend(movie_name: str):
    if movies is not None and similarity is not None:
        try:
            user_input = movie_name.strip()
            
            find_close_match = difflib.get_close_matches(user_input, list_of_all_titles, n=1, cutoff=0.2)
            
            if not find_close_match:
                return {"error": f"Maaf kijiyega, '{user_input}' se milti-julti koi movie/show nahi mila. Kripya thoda sahi naam likhein."}
            
            close_match = find_close_match[0]
            
            index_of_movie = movies[movies.title == close_match].index[0]
            
            similarity_score = list(enumerate(similarity[index_of_movie]))
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
            
            recommended_movies = []
            for movie in sorted_similar_movies:
                index = movie[0]
                title_from_index = movies.iloc[index]['title']
                
                if title_from_index.lower() == close_match.lower():
                    continue
                
                recommended_movies.append(title_from_index)
                
                if len(recommended_movies) == 10: 
                    break
                    
            return {
                "searched_movie": close_match, 
                "recommendations": recommended_movies
            }
            
        except Exception as err:
            return {"error": f"Recommendation process mein dikkat aayi: {str(err)}"}
            
    else:
        movie_clean = movie_name.strip().lower()
        if movie_clean in MOCK_DATABASE:
            return {
                "searched_movie": movie_name,
                "recommendations": MOCK_DATABASE[movie_clean]
            }
        else:
            return {"error": "Movie nahi mila. Testing ke liye 'Inception' ya 'Avatar' daalein."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)