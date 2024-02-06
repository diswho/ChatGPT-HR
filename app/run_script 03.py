# https://www.geeksforgeeks.org/how-to-insert-image-in-sqlite-using-python/
import sqlite3
import os
from passlib.context import CryptContext
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_LOCAL = "sqlite:///./local.db"
# Function for Convert Binary Data
# to Human Readable Format
filename = os.path.abspath(__file__)
# 'C:\\Users\\phuong\\Documents\\Workspaces\\Python\\ChatGPT-HR\\app\\run_script.py'
DATABASE_URL_EXTERNAL = r'C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db'
DATABASE_URL_LOCAL = 'local.db'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def insertBLOB():
    connectionExternal = None
    connectionLocal = None
    try:
        connectionExternal = sqlite3.connect(DATABASE_URL_EXTERNAL)
        connectionLocal = sqlite3.connect(DATABASE_URL_LOCAL)

        cursorExternal = connectionExternal.cursor()
        cursorLocal = connectionLocal.cursor()

        sqlite_selet = '''SELECT  id, emp_pin, emp_ssn, emp_firstname, emp_lastname, emp_phone, emp_photo, emp_privilege, emp_hiredate, emp_address, emp_active, emp_firedate, emp_firereason, emp_emergencyphone1, emp_emergencyphone2, emp_emergencyname, emp_emergencyaddress, emp_cardNumber, emp_country, emp_city, emp_state, emp_email, emp_title, emp_hourlyrate1, emp_hourlyrate2, emp_hourlyrate3, emp_hourlyrate4, emp_hourlyrate5, emp_gender, emp_birthday, emp_operationmode, emp_Line, emp_Passport, emp_MotobikeLicence, emp_CarLicence, IsSelect, middleware_id, nationalID, emp_Verify, emp_ViceCard, department_id, position_id FROM hr_employee limit 10'''
        data1 = cursorExternal.execute(sqlite_selet)

        connectionLocal.execute('''CREATE TABLE IF NOT EXISTS Student
         (id integer ,	full_name TEXT,	email TEXT,	hashed_password TEXT,	is_active BOOLEAN,	is_superuser BOOLEAN,	emp_pin TEXT PRIMARY KEY,	emp_ssn TEXT,	emp_role TEXT,	emp_firstname TEXT NOT NULL,	emp_lastname TEXT,	emp_username TEXT,	emp_pwd TEXT,	emp_timezone TEXT,	emp_phone TEXT,	emp_payroll_id TEXT,	emp_payroll_type TEXT,	emp_pin2 TEXT,	emp_photo BLOB,	emp_privilege TEXT,	emp_group TEXT,	emp_hiredate DATETIME,	emp_address TEXT,	emp_active INT NOT NULL,	emp_firedate DATETIME,	emp_firereason TEXT,	emp_emergencyphone1 TEXT,	emp_emergencyphone2 TEXT,	emp_emergencyname TEXT,	emp_emergencyaddress TEXT,	emp_cardNumber TEXT,	emp_country TEXT,	emp_city TEXT,	emp_state TEXT,	emp_postal TEXT,	emp_fax TEXT,	emp_email TEXT,	emp_title TEXT,	emp_hourlyrate1 NUMERIC,	emp_hourlyrate2 NUMERIC,	emp_hourlyrate3 NUMERIC,	emp_hourlyrate4 NUMERIC,	emp_hourlyrate5 NUMERIC,	emp_gender INT,	emp_birthday DATETIME,	emp_operationmode INT,	emp_OtherName TEXT,	emp_Line TEXT,	emp_Passport TEXT,	emp_MotobikeLicence TEXT,	emp_CarLicence TEXT,	emp_customName1 TEXT,	emp_customInfo1 TEXT,	emp_customName2 TEXT,	emp_customInfo2 TEXT,	IsSelect INT,	middleware_id BIGINT,	nationalID TEXT,	emp_Verify TEXT,	emp_ViceCard TEXT,	department_id INT,	position_id INT)
         ''')

        # insert query
        for orig_raw in data1:
            # print(raw)
            list_raw = list(orig_raw)
            list_raw.insert(1, orig_raw[3]+" "+orig_raw[4])
            list_raw.insert(2, orig_raw[1] + "@mail.com")
            list_raw.insert(3,  pwd_context.hash(orig_raw[1]))
            list_raw.insert(4,  True)
            list_raw.insert(5,  False)
            new_raw=tuple(list_raw)
            # print("=== new_raw: ",new_raw) 
            sqlite_insert = """INSERT INTO Student
            (id, full_name, email, hashed_password, is_active, is_superuser, emp_pin, emp_ssn, emp_firstname, emp_lastname, emp_phone, emp_photo, emp_privilege, emp_hiredate, emp_address, emp_active, emp_firedate, emp_firereason, emp_emergencyphone1, emp_emergencyphone2, emp_emergencyname, emp_emergencyaddress, emp_cardNumber, emp_country, emp_city, emp_state, emp_email, emp_title, emp_hourlyrate1, emp_hourlyrate2, emp_hourlyrate3, emp_hourlyrate4, emp_hourlyrate5, emp_gender, emp_birthday, emp_operationmode, emp_Line, emp_Passport, emp_MotobikeLicence, emp_CarLicence, IsSelect, middleware_id, nationalID, emp_Verify, emp_ViceCard, department_id, position_id) VALUES
            (?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?)"""
        # using cursor object executing our query
            cursorLocal.execute(sqlite_insert, new_raw)
            connectionLocal.commit()
        # connectionExternal.commit()
        print("========= inserted successfully into a table")
        cursorLocal.close()
        cursorExternal.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if connectionLocal:
            connectionLocal.close()
            print("========= the sqlite connection is closed")
        if connectionExternal:
            connectionExternal.close()
            print("========= the sqlite connection is closed")


insertBLOB()
