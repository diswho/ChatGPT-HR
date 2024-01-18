from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from databases import Database
from sqlalchemy.orm import sessionmaker

# Create databases
DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

# Create the FastAPI app
app = FastAPI()

# Database Dependency


def get_database(database_url: str):
    database = Database(database_url)
    return database


def get_engine(database: Database = Depends(get_database)):
    # Use str() to ensure the URL is in string format
    engine = create_engine(str(database.url))
    return engine


# Dependency for external database
get_database_external = get_database(DATABASE_URL_EXTERNAL)
get_engine_external = get_engine(get_database_external)

# Dependency for local database
get_database_local = get_database(DATABASE_URL_LOCAL)
get_engine_local = get_engine(get_database_local)

# Dependency for creating a session
SessionExternal = sessionmaker(
    autocommit=False, autoflush=False, bind=get_engine_external)


@app.get("/users/{user_id}")
async def read_user_external(user_id: int):
    query = text("SELECT * FROM hr_employee WHERE id = :user_id")

    # Use the session from SessionLocal for database operations
    with SessionExternal() as session:
        result = session.execute(query, {"user_id": user_id}).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = dict(result)
    return user
