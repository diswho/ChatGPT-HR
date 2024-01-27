from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from databases import Database

from typing import Any
# from sqlalchemy import create_engine, text
from sqlalchemy import Boolean, Column,  Integer, String, ForeignKey, create_engine, text
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from pydantic import BaseModel, EmailStr
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


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
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None
    remark: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


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
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

# Replace with a strong secret key
SECRET_KEY = "f3bc724a1cbd9b106f929c4bf246514862e3ed34fb117248c215de24bcd898c0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    hashed_password = pwd_context.hash(user.hashed_password)
    db_user = User(email=user.email,
                   hashed_password=hashed_password,
                   full_name=user.full_name,
                   is_superuser=user.is_superuser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    # Retrieve the user by user_id
    user = db.query(User).filter(User.id == user_id).first()

    # Check if the user exists
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify hashed password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get a user by email


def get_user(db, email: str):
    return db.query(User).filter(User.email == email).first()

# Dependency for token verification


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_lcl)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # token_data = {"sub": email}
        # token_data = {"sub": email}
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    # me = get_user(db, email)
    user = get_user(db, email=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# TODO: Check if any update
# Get Info of each employee, Summary


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_lcl)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token,
            "token_type": "bearer",
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "full_name": user.full_name,
            "user_id": user.id}


@app.get("/users/me", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_user)):

    return current_user


@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_lcl), current_user: UserBase = Depends(get_current_user)):

    return delete_user(db=db, user_id=user_id)


@app.post("/users/{user_id}", response_model=UserCreate)
async def insert_user(user_id: int, db: Session = Depends(get_lcl), current_user: UserBase = Depends(get_current_user)):

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
async def read_external_user(user_id: int, current_user: UserBase = Depends(get_current_user)):

    query = text("SELECT * FROM hr_employee WHERE id = :user_id")
    with SessionExternal() as session:
        result = session.execute(query, {"user_id": user_id}).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = dict(result)
    return user
