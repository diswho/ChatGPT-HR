from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database 1 Configuration
DATABASE_URL_1 = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_1 = "sqlite:///C:\Users\phuong\OneDrive\Private\Xokthavi\HR"
engine1 = create_engine(DATABASE_URL_1)
Session1 = sessionmaker(autocommit=False, autoflush=False, bind=engine1)
Base1 = declarative_base()

# Database 2 Configuration
DATABASE_URL_2 = "sqlite:///./test2.db"
engine2 = create_engine(DATABASE_URL_2)
Session2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)
Base2 = declarative_base()

# Example Model for Database 1


# class Item1(Base1):
#     __tablename__ = "hr_employee"
#     id = Column(Integer, primary_key=True, index=True)
#     emp_pin = Column(String, index=True)

# # Example Model for Database 2


# class Item2(Base2):
#     __tablename__ = "hr_employee"
#     id = Column(Integer, primary_key=True, index=True)
#     emp_pin = Column(String, index=True)


# Create tables in databases
Base1.metadata.create_all(bind=engine1)
Base2.metadata.create_all(bind=engine2)

# Dependency to get a session for Database 1


def get_db1():
    db1 = Session1()
    try:
        yield db1
    finally:
        db1.close()

# Dependency to get a session for Database 2


def get_db2():
    db2 = Session2()
    try:
        yield db2
    finally:
        db2.close()

# Endpoint to read from Database 1 and write to Database 2


@app.post("/copy_item/")
async def copy_item(item_id: int, db1: Session1 = Depends(get_db1)):
# async def copy_item(item_id: int, db1: Session1 = Depends(get_db1), db2: Session2 = Depends(get_db2)):
    # Read from Database 1
    # item1 = db1.query(Item1).filter(Item1.id == item_id).first()
    query = text(f"SELECT * FROM hr_employee WHERE id = {item_id}")
    item11 = db1.execute(query).fetchone()
    if item11 is None:
        raise HTTPException(
            status_code=404, detail="Item not found in Database 1")

    # Write to Database 2

    # item2 = Item2(name=item11.name)
    # db2.add(item2)
    # db2.commit()
    # db2.refresh(item2)

    # return item2
    user = dict(item11)
    return user
