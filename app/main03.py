from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Database 1 Configuration
DATABASE_URL_1 = "sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
engine1 = create_engine(DATABASE_URL_1)
Session1 = sessionmaker(autocommit=False, autoflush=False, bind=engine1)

# Database 2 Configuration
DATABASE_URL_2 = "sqlite:///./test2.db"
engine2 = create_engine(DATABASE_URL_2)
Session2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

# SessionLocal class with thread_local


class SessionLocal:
    def __init__(self, engine):
        self.session = None
        self.engine = engine

    def __enter__(self):
        self.session = Session(
            autocommit=False, autoflush=False, bind=self.engine)
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session:
            self.session.close()

# Dependency to get a session for Database 1


def get_db1():
    db1 = Session1(engine1)
    try:
        yield db1
    finally:
        db1.close()

# Dependency to get a session for Database 2


def get_db2():
    db2 = Session2(engine2)
    try:
        yield db2
    finally:
        db2.close()

# Endpoint to read from Database 1 and write to Database 2


@app.post("/copy_item/")
async def copy_item(item_id: int, db1: Session = Depends(get_db1), db2: Session = Depends(get_db2)):
    # Read from Database 1
    query = text(f"SELECT * FROM hr_employee WHERE id = {item_id}")
    item1 = db1.execute(query).fetchone()
    if item1 is None:
        raise HTTPException(
            status_code=404, detail="Item not found in Database 1")

    # Write to Database 2
    with db2.begin():
        # Perform the necessary operations here using db2
        # For example: db2.execute(some_query)
        pass

    # For now, just returning the user as a dictionary
    user = dict(item1)
    return user


@app.post("/show_item/")
async def show_item(item_id: int, db1: Session = Depends(get_db1), db2: Session = Depends(get_db2)):
    query = text(f"SELECT * FROM hr_employee WHERE id = {item_id}")
    item1 = db1.execute(query).fetchone()
    return "Success"
