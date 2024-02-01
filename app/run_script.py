from fastapi import FastAPI, HTTPException, Depends
import sqlite3
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

app = FastAPI()

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
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=get_engine_local)

@app.get("/run-script")
def run_script_endpoint():
    query1 = "SELECT * FROM hr_employee;"
    data1 = SessionExternal().execute(query1).fetchall()
    for row1 in data1:
        print(row1)
    # run_script()
    return {"message": "Script executed successfully"}

# Define other routes for your API
# Example: CRUD operations on the database


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
