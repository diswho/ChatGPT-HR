from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

app = FastAPI()

# Define database models for both databases
Base = declarative_base()


class SourceModel(Base):
    __tablename__ = "source_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class DestinationModel(Base):
    __tablename__ = "destination_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


# Configure database URLs
source_db_url = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# source_db_url = "sqlite:///source.db"
destination_db_url = "sqlite:///destination.db"

# Create database connections
source_database = Database(source_db_url)
destination_database = Database(destination_db_url)

# Dependency to get a database connection


async def get_db():
    db = source_database
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

# Endpoint to copy data from source to destination


@app.get("/copy-database")
async def copy_database(db: Database = Depends(get_db)):
    # Query data from the source database
    source_data = await db.fetch_all(select(SourceModel))

    # Connect to the destination database
    await destination_database.connect()

    # Insert or update data into the destination database
    for row in source_data:
        destination_row = DestinationModel(**row)
        await destination_database.execute(DestinationModel.__table__.insert().values(destination_row))

    # Disconnect from the destination database
    await destination_database.disconnect()

    return {"message": "Database copied successfully"}
