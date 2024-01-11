from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from databases import Database

DATABASE_URL = r"sqlite:///c:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\XokThaVi.db"

# Create the FastAPI app
app = FastAPI()

# Database Dependency


def get_database():
    database = Database(DATABASE_URL)
    return database

# Dependency to get the SQLAlchemy engine


def get_engine(database: Database = Depends(get_database)):
    engine = create_engine(DATABASE_URL)
    return engine

# Define a FastAPI endpoint to read data from the SQLite database using raw SQL


@app.get("/users/{user_id}")
async def read_user(user_id: int, engine=Depends(get_engine)):
    query = text(f"SELECT * FROM hr_employee WHERE id = {user_id}")
    result = engine.execute(query).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = dict(result)
    return user
