from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import random

# Creamos la aplicación FastAPI
app = FastAPI()

# Simulamos una base de datos en memoria para las películas y sus puntuaciones
movies_db = {
    1: {"title": "Inception", "ratings": []},
    2: {"title": "The Matrix", "ratings": []},
    3: {"title": "The Dark Knight", "ratings": []},
}

# Modelo para las puntuaciones
class Rating(BaseModel):
    score: int  # Puntuación entre 1 y 10

# Ruta para obtener todas las películas
@app.get("/movies")
def get_movies():
    return {"movies": [{"id": movie_id, "title": movie["title"]} for movie_id, movie in movies_db.items()]}

# Ruta para calificar una película
@app.post("/movies/{movie_id}/rate")
def rate_movie(movie_id: int, rating: Rating):
    if movie_id not in movies_db:
        return {"error": "Movie not found"}
    
    if 1 <= rating.score <= 10:
        movies_db[movie_id]["ratings"].append(rating.score)
        return {"message": "Rating added successfully"}
    else:
        return {"error": "Rating must be between 1 and 10"}

# Ruta para obtener el promedio de puntuación de una película
@app.get("/movies/{movie_id}/average")
def get_average_rating(movie_id: int):
    if movie_id not in movies_db:
        return {"error": "Movie not found"}
    
    ratings = movies_db[movie_id]["ratings"]
    if ratings:
        average = sum(ratings) / len(ratings)
        return {"average_rating": round(average, 2)}
    else:
        return {"average_rating": "No ratings yet"}
