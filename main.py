from typing import Optional, List
from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "My app with FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@example.com":
            raise HTTPException(status_code=403, detail="Invalid credentials")

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="My movie",min_legth=5, max_length=15)
    overview: str = Field(default="Description",min_legth=15, max_length=50)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_legth=5, max_length=15)

    class Config:
        json_schema_extra = {
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

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello, World!</h1>")

@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@example.com" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)

@app.get("/movies/{movie_id}", tags=["movies"], response_model=Movie)
def get_movie(movie_id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        return JSONResponse(content={"error": "Movie not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created"}, status_code=201)

@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"error": "Movie not found"}, status_code=404)
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content={"message": "Movie updated"}, status_code=200)


@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200) 
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"error": "Movie not found"}, status_code=404)
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Movie deleted"}, status_code=200)