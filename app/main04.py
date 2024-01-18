from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from databases import Database
# Create databases
DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

# Create the FastAPI app
app = FastAPI()

# Database Dependency


def get_database_external():
    database = Database(DATABASE_URL_EXTERNAL)
    return database


def get_engine_external(database: Database = Depends(get_database_external)):
    engine = create_engine(DATABASE_URL_EXTERNAL)
    return engine


def get_database_local():
    database = Database(DATABASE_URL_LOCAL)
    return database


def get_engine_local(database: Database = Depends(get_database_local)):
    engine = create_engine(DATABASE_URL_LOCAL)
    return engine


@app.get("/users/{user_id}")
async def read_user_external(user_id: int, engine=Depends(get_engine_external)):
    query = text(f"SELECT * FROM hr_employee WHERE id = {user_id}")
    result = engine.execute(query).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = dict(result)
    return user
