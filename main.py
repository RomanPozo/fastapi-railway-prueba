from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Lista de usuarios en memoria (simula una base de datos)
users_db = []

# Definimos el modelo de datos para el usuario
class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    age: int

# Ruta para crear un usuario
@app.post("/users/", response_model=User)
def create_user(user: User):
    users_db.append(user)  # Agregar el usuario a la lista
    return user

# Ruta para obtener todos los usuarios
@app.get("/users/", response_model=List[User])
def get_users():
    return users_db

# Ruta para eliminar un usuario por su username
@app.delete("/users/{username}", response_model=User)
def delete_user(username: str):
    for user in users_db:
        if user.username == username:
            users_db.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User not found")

