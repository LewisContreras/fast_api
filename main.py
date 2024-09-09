from typing import Optional, List
from urllib import response
from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="My movie",min_legth=5, max_length=15)
    overview: str = Field(default="Description",min_legth=15, max_length=50)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_legth=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My movie",
                "overview": "Description",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": 2009,
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": 2009,
        "rating": 7.8,
        "category": "Acción"
    },
]

app.title = "My app with FastAPI"
app.version = "0.0.1"

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello, World!</h1>")

@app.get("/movies", tags=["movies"], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

@app.get("/movies/{movie_id}", tags=["movies"], response_model=Movie)
def get_movie(movie_id: int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == movie_id:
            return JSONResponse(content=movie)
    return JSONResponse(content={"error": "Movie not found"}, status_code=404)

@app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [ movie for movie in movies if movie["category"] == category ]
    return JSONResponse(content=data)

@app.post("/movies", tags=["movies"], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie.model_dump())
    return JSONResponse(content={"message": "Movie created"})

@app.put("/movies/{id}", tags=["movies"], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Movie updated"})
    return {"error": "Movie not found"}

@app.delete("/movies/{id}", tags=["movies"], response_model=dict)   
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(content={"message": "Movie deleted"})
    return {"error": "Movie not found"}