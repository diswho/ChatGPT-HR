from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from databases import Database
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import logging

# Create databases
DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create the FastAPI app
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


@app.get("/update_users")
async def update_users(db: Session = Depends(get_ext)):
    qry_sel = text('''SELECT  id, emp_pin, emp_ssn, emp_firstname, emp_lastname, emp_phone, emp_photo, emp_privilege, emp_hiredate, emp_address, emp_active, emp_firedate, emp_firereason, emp_emergencyphone1, emp_emergencyphone2, emp_emergencyname, emp_emergencyaddress, emp_cardNumber, emp_country, emp_city, emp_state, emp_email, emp_title, emp_hourlyrate1, emp_hourlyrate2, emp_hourlyrate3, emp_hourlyrate4, emp_hourlyrate5, emp_gender, emp_birthday, emp_operationmode, emp_Line, emp_Passport, emp_MotobikeLicence, emp_CarLicence, IsSelect, middleware_id, nationalID, emp_Verify, emp_ViceCard, department_id, position_id FROM hr_employee limit 10''')
    qry_create = '''CREATE TABLE IF NOT EXISTS Student
         (id integer ,	full_name TEXT,	email TEXT,	hashed_password TEXT,	is_active BOOLEAN,	is_superuser BOOLEAN,	emp_pin TEXT PRIMARY KEY,	emp_ssn TEXT,	emp_role TEXT,	emp_firstname TEXT NOT NULL,	emp_lastname TEXT,	emp_username TEXT,	emp_pwd TEXT,	emp_timezone TEXT,	emp_phone TEXT,	emp_payroll_id TEXT,	emp_payroll_type TEXT,	emp_pin2 TEXT,	emp_photo BLOB,	emp_privilege TEXT,	emp_group TEXT,	emp_hiredate DATETIME,	emp_address TEXT,	emp_active INT NOT NULL,	emp_firedate DATETIME,	emp_firereason TEXT,	emp_emergencyphone1 TEXT,	emp_emergencyphone2 TEXT,	emp_emergencyname TEXT,	emp_emergencyaddress TEXT,	emp_cardNumber TEXT,	emp_country TEXT,	emp_city TEXT,	emp_state TEXT,	emp_postal TEXT,	emp_fax TEXT,	emp_email TEXT,	emp_title TEXT,	emp_hourlyrate1 NUMERIC,	emp_hourlyrate2 NUMERIC,	emp_hourlyrate3 NUMERIC,	emp_hourlyrate4 NUMERIC,	emp_hourlyrate5 NUMERIC,	emp_gender INT,	emp_birthday DATETIME,	emp_operationmode INT,	emp_OtherName TEXT,	emp_Line TEXT,	emp_Passport TEXT,	emp_MotobikeLicence TEXT,	emp_CarLicence TEXT,	emp_customName1 TEXT,	emp_customInfo1 TEXT,	emp_customName2 TEXT,	emp_customInfo2 TEXT,	IsSelect INT,	middleware_id BIGINT,	nationalID TEXT,	emp_Verify TEXT,	emp_ViceCard TEXT,	department_id INT,	position_id INT)
         '''
    qry_ist = """INSERT INTO Student
            (emp_pin, emp_firstname, emp_active) VALUES
            (:emp_pin, :emp_firstname, :emp_active)"""
    # qry_ist = """INSERT INTO Student
    #         (id, full_name, email, hashed_password, is_active, is_superuser, emp_pin, emp_ssn, emp_firstname, emp_lastname, emp_phone, emp_photo, emp_privilege, emp_hiredate, emp_address, emp_active, emp_firedate, emp_firereason, emp_emergencyphone1, emp_emergencyphone2, emp_emergencyname, emp_emergencyaddress, emp_cardNumber, emp_country, emp_city, emp_state, emp_email, emp_title, emp_hourlyrate1, emp_hourlyrate2, emp_hourlyrate3, emp_hourlyrate4, emp_hourlyrate5, emp_gender, emp_birthday, emp_operationmode, emp_Line, emp_Passport, emp_MotobikeLicence, emp_CarLicence, IsSelect, middleware_id, nationalID, emp_Verify, emp_ViceCard, department_id, position_id) VALUES
    #         (?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?)"""

    try:

        ssnExt = SessionExternal()
        ssnLoc = SessionLocal()

        res_Ext = ssnExt.execute(qry_sel).fetchall()
        ssnLoc.execute(qry_create)
        for orig_raw in res_Ext:
            list_raw = list(orig_raw)
            list_raw.insert(1, orig_raw[3]+" "+orig_raw[4])
            list_raw.insert(2, orig_raw[1] + "@mail.com")
            list_raw.insert(3,  pwd_context.hash(orig_raw[1]))
            list_raw.insert(4,  True)
            list_raw.insert(5,  False)
            new_raw = {'emp_pin': orig_raw[1], 'emp_firstname': orig_raw[3], 'emp_active': 1}
            print(new_raw)
            # ssnLoc.execute(qry_ist, **new_raw)
            get_engine_local.execute(qry_ist, **new_raw)

    except ValueError as e:
        logging.error("ValueError occurred:", exc_info=True)
    except Exception as e:
        logging.error("An unexpected error occurred:", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to update users: {str(e)}")
    finally:
        ssnExt.close()
        ssnLoc.close()
    return "Success"
