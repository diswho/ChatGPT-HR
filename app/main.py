from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from databases import Database

from typing import Any
# from sqlalchemy import create_engine, text
from sqlalchemy import Boolean, Column,  Integer, String, ForeignKey, create_engine, text, DateTime,  Numeric, BigInteger
from sqlalchemy.types import LargeBinary
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
    emp_pin = Column(String, nullable=False)
    emp_ssn = Column(String)
    emp_firstname = Column(String, nullable=False)
    emp_lastname = Column(String)
    emp_phone = Column(String)
    emp_photo = Column(LargeBinary)
    emp_privilege = Column(String)
    emp_hiredate = Column(DateTime)
    emp_address = Column(String)
    emp_active = Column(Integer, nullable=False)
    emp_firedate = Column(DateTime)
    emp_firereason = Column(String)
    emp_emergencyphone1 = Column(String)
    emp_emergencyphone2 = Column(String)
    emp_emergencyname = Column(String)
    emp_emergencyaddress = Column(String)
    emp_cardNumber = Column(String)
    emp_country = Column(String)
    emp_city = Column(String)
    emp_state = Column(String)
    emp_email = Column(String)
    emp_title = Column(String)
    emp_hourlyrate1 = Column(Integer)
    emp_hourlyrate2 = Column(Integer)
    emp_hourlyrate3 = Column(Integer)
    emp_hourlyrate4 = Column(Integer)
    emp_hourlyrate5 = Column(Integer)
    emp_gender = Column(Integer)
    emp_birthday = Column(DateTime)
    emp_operationmode = Column(Integer)
    emp_Line = Column(String)
    emp_Passport = Column(String)
    emp_MotobikeLicence = Column(String)
    emp_CarLicence = Column(String)
    IsSelect = Column(Integer)
    middleware_id = Column(Integer)
    nationalID = Column(String)
    emp_Verify = Column(String)
    emp_ViceCard = Column(String)
    department_id = Column(Integer)
    position_id = Column(Integer)


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None
    remark: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    hashed_password: str


class UserInDB(UserBase):
    id: int
    hashed_password: Optional[str] = None
    emp_pin: Optional[str] = None
    emp_firstname: Optional[str] = None
    emp_lastname: Optional[str] = None
    emp_active: int
    items: Optional[list] = None
    roles: Optional[list] = None
    emp_ssn: Optional[str] = None
    emp_phone: Optional[str] = None
    emp_photo: Optional[bytes] = None
    emp_privilege: Optional[str] = None
    emp_hiredate: Optional[datetime] = None
    emp_address: Optional[str] = None
    emp_firedate: Optional[datetime] = None
    emp_firereason: Optional[str] = None
    emp_emergencyphone1: Optional[str] = None
    emp_emergencyphone2: Optional[str] = None
    emp_emergencyname: Optional[str] = None
    emp_emergencyaddress: Optional[str] = None
    emp_cardNumber: Optional[str] = None
    emp_country: Optional[str] = None
    emp_city: Optional[str] = None
    emp_state: Optional[str] = None
    emp_email: Optional[str] = None
    emp_title: Optional[str] = None
    emp_hourlyrate1: Optional[int] = None
    emp_hourlyrate2: Optional[int] = None
    emp_hourlyrate3: Optional[int] = None
    emp_hourlyrate4: Optional[int] = None
    emp_hourlyrate5: Optional[int] = None
    emp_gender: Optional[int] = None
    emp_birthday: Optional[datetime] = None
    emp_operationmode: Optional[int] = None
    emp_Line: Optional[str] = None
    emp_Passport: Optional[str] = None
    emp_MotobikeLicence: Optional[str] = None
    emp_CarLicence: Optional[str] = None
    IsSelect: Optional[int] = None
    middleware_id: Optional[int] = None
    nationalID: Optional[str] = None
    emp_Verify: Optional[str] = None
    emp_ViceCard: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None


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


@app.get("/users")
async def database_comparing(db: Session = Depends(get_lcl), current_user: UserBase = Depends(get_current_user)):
    query_ext = text("""
                 SELECT id,emp_pin,emp_ssn,emp_firstname,emp_lastname,emp_phone,emp_photo,emp_privilege,
                 emp_hiredate,emp_address,emp_active,emp_firedate,emp_firereason,emp_emergencyphone1,emp_emergencyphone2,emp_emergencyname,emp_emergencyaddress,
                 emp_cardNumber,emp_country,emp_city,emp_state,emp_email,emp_title,emp_hourlyrate1,emp_hourlyrate2,emp_hourlyrate3,emp_hourlyrate4,emp_hourlyrate5,
                 emp_gender,emp_birthday,emp_operationmode,emp_Line,emp_Passport,emp_MotobikeLicence,emp_CarLicence,IsSelect,middleware_id,
                 nationalID,emp_Verify,emp_ViceCard,department_id,position_id
                 FROM "hr_employee" ;
                 """)
    query_int = text("""
                 SELECT id,emp_pin,emp_ssn,emp_firstname,emp_lastname,emp_phone,emp_photo,emp_privilege,
                 emp_hiredate,emp_address,emp_active,emp_firedate,emp_firereason,emp_emergencyphone1,emp_emergencyphone2,emp_emergencyname,emp_emergencyaddress,
                 emp_cardNumber,emp_country,emp_city,emp_state,emp_email,emp_title,emp_hourlyrate1,emp_hourlyrate2,emp_hourlyrate3,emp_hourlyrate4,emp_hourlyrate5,
                 emp_gender,emp_birthday,emp_operationmode,emp_Line,emp_Passport,emp_MotobikeLicence,emp_CarLicence,IsSelect,middleware_id,
                 nationalID,emp_Verify,emp_ViceCard,department_id,position_id
                 FROM "user" ;
                     """)
    data1 = SessionExternal().execute(query_ext).fetchall()
    data2 = SessionLocal().execute(query_int).fetchall()

    for row in data1:
        is_new_record = True
        for i, record in enumerate(data2):
            if record[1] == row[1]:
                # Update existing record
                data2[i] = row
                is_new_record = False
            break
        # If the record is not found, add it to the list
        if is_new_record:
            SessionLocal().execute("INSERT INTO user (id,full_name,email,hashed_password,is_active,is_superuser,emp_pin,emp_ssn,emp_firstname,emp_lastname,emp_phone,emp_photo,emp_privilege,emp_hiredate,emp_address,emp_active,emp_firedate,emp_firereason,emp_emergencyphone1,emp_emergencyphone2,emp_emergencyname,emp_emergencyaddress, emp_cardNumber,emp_country,emp_city,emp_state,emp_email,emp_title,emp_hourlyrate1,emp_hourlyrate2,emp_hourlyrate3,emp_hourlyrate4,emp_hourlyrate5, emp_gender,emp_birthday,emp_operationmode,emp_Line,emp_Passport,emp_MotobikeLicence,emp_CarLicence,IsSelect,middleware_id,nationalID,emp_Verify,emp_ViceCard,department_id,position_id) VALUES (?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?)",
                                   (row[0],	row[3]+" " + row[4], row[1]+"@mail.com", pwd_context.hash("1234"), True, False, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41]))
            # records.append(new_record)

    # for row1 in data1:
    #     # Check if row exists in table2
    #     if row1 not in data2:
    #         print("New Record found in table1:", row1)
    #     else:
    #         # Compare each field to identify updates
    #         index = data2.index(row1)
    #         for i in range(len(row1)):
    #             if row1[i] != data2[index][i]:
    #                 print("Updated Record found:", row1, "->", data2[index])

    return "Success"
