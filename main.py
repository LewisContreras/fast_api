from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
]

app.title = "My app with FastAPI"
app.version = "0.0.1"

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello, World!</h1>")

@app.get("/movies", tags=["movies"])
def get_movies():
    return movies

@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"error": "Movie not found"}

@app.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str):
    movies_by_category = []
    for movie in movies:
        if movie["category"] == category:
            movies_by_category.append(movie)
    return movies_by_category