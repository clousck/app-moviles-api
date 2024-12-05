from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import database

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str

app = FastAPI()

@app.get("/")
def get_root():
    return {"message": "FastAPI root"}

# CRUD Operations

@app.get("/users", response_model=List[User])
def get_users():
    query = "SELECT id, name, email FROM users"
    users = database.execute_query(query)
    if "error" in users:
        raise HTTPException(status_code=500, detail=users["error"])
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    query = f"SELECT id, name, email FROM users WHERE id = {user_id}"
    users = database.execute_query(query)
    if "error" in users:
        raise HTTPException(status_code=500, detail=users["error"])
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[0]

@app.post("/users", response_model=User)
def create_user(user: User):
    query = f"INSERT INTO users (name, email) VALUES ('{user.name}', '{user.email}')"
    result = database.execute_non_query(query)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return {"id": None, "name": user.name, "email": user.email}

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    query = f"""
        UPDATE users
        SET name = '{user.name}', email = '{user.email}'
        WHERE id = {user_id}
    """
    result = database.execute_non_query(query)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return {"id": user_id, "name": user.name, "email": user.email}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    query = f"DELETE FROM users WHERE id = {user_id}"
    result = database.execute_non_query(query)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return {"message": f"User with ID {user_id} deleted successfully"}
