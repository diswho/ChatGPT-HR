from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException
import databases
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text

# Create databases
DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

# engine_external = create_engine(DATABASE_URL_EXTERNAL)
# database_external = databases.Database(DATABASE_URL_EXTERNAL)
# metadata_external = MetaData()

# engine_local = create_engine(DATABASE_URL_LOCAL)
# database_local = databases.Database(DATABASE_URL_LOCAL)
# metadata_local = MetaData()


def get_database_external():
    database = databases.Database(DATABASE_URL_EXTERNAL)
    return database


def get_engine_external(database: databases.Database = Depends(get_database_external)):
    engine = create_engine(DATABASE_URL_EXTERNAL)
    return engine


def get_database_local():
    database = databases.Database(DATABASE_URL_LOCAL)
    return database


def get_engine_local(database: databases.Database = Depends(get_database_local)):
    engine = create_engine(DATABASE_URL_LOCAL)
    return engine


app = FastAPI()


# @app.on_event("startup")
# async def startup_db():
#     await database_external.connect()
#     await database_local.connect()


# @app.on_event("shutdown")
# async def shutdown_db():
#     await database_external.disconnect()
#     await database_local.disconnect()


# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}


# employee_external = Table(
#     "employee",
#     metadata_external,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("name", String),
#     Column("attendance_info", String),
# )

# department_external = Table(
#     "department",
#     metadata_external,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("name", String),
# )


@app.get("/employees/{employee_id}")
async def read_employee(employee_id: int, engine=Depends(get_engine_external)):
    query = text(f"SELECT * FROM hr_employee WHERE id = {employee_id}")
    result = engine.execute(query).fetchone()
    # query = employee_external.select().where(employee_external.c.id == employee_id)
    # result = await database_external.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result
