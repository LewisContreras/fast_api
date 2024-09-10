from typing import Optional
from pydantic import BaseModel, Field

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