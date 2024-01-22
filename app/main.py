from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from databases import Database
from sqlalchemy.orm import sessionmaker

from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Boolean, Column,  Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.associationproxy import association_proxy
from typing import Optional
from sqlalchemy.orm import Session


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
    roles = relationship("RoleUser", back_populates="user")


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional [bool] = False
    full_name: Optional[str] = None
    remark: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    hashed_password: str


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    users = relationship("RoleUser", back_populates="role")


class RoleUser(Base):
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    role_id = Column(ForeignKey('role.id'), primary_key=True)
    remark = Column(String, nullable=False)
    role = relationship("Role", back_populates="users")
    user = relationship("User", back_populates="roles")
    # proxies
    role_name = association_proxy(target_collection='role', attr="name")
    user_name = association_proxy(target_collection='user', attr="full_name")


# Create databases
DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
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
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=get_engine_local)


def get_ext():
    db = SessionExternal()
    try:
        yield db
    finally:
        db.close


def get_lcl():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


def create(db: Session, user: UserCreate) -> Optional[User]:
    db_user = User(email=user.email,
                   hashed_password="get_password_hash "+user.hashed_password,
                   #    hashed_password=get_password_hash(user.hashed_password),
                   full_name=user.full_name,
                   is_superuser=user.is_superuser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/users/{user_id}", response_model=UserCreate)
async def insert_user(user_id: int, db: Session = Depends(get_lcl)):
    query = text("SELECT * FROM hr_employee WHERE id = :user_id")

    with SessionExternal() as session:
        result = session.execute(query, {"user_id": user_id}).fetchone()
    new_user = UserCreate
    new_user.email = result[1]+"@email.com"
    new_user.hashed_password = "hashed_password"
    new_user.full_name = result[4]
    new_user.is_superuser = True
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    create_user = create(db=db, user=new_user)
    # user = dict(result)
    # return user
    return create_user


@app.get("/users/{user_id}")
async def read_user_external(user_id: int):
    query = text("SELECT * FROM hr_employee WHERE id = :user_id")

    # Use the session from SessionLocal for database operations
    # with SessionExternal() as session:
    #     result = session.execute(query, {"user_id": user_id}).fetchone()
    with SessionExternal() as session:
        result = session.execute(query, {"user_id": user_id}).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = dict(result)
    return user
