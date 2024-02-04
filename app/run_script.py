# https://www.geeksforgeeks.org/how-to-insert-image-in-sqlite-using-python/
import sqlite3
import os
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_LOCAL = "sqlite:///./local.db"
# Function for Convert Binary Data
# to Human Readable Format
filename = os.path.abspath(__file__)
# 'C:\\Users\\phuong\\Documents\\Workspaces\\Python\\ChatGPT-HR\\app\\run_script.py'
DATABASE_URL_EXTERNAL = r'C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db'
DATABASE_URL_LOCAL = 'local.db'


def insertBLOB():
    try:
        connectionExternal = sqlite3.connect(DATABASE_URL_EXTERNAL)
        connectionLocal = sqlite3.connect(DATABASE_URL_LOCAL)

        cursorExternal = connectionExternal.cursor()
        cursorLocal = connectionLocal.cursor()

        sqlite_selet = '''SELECT  id, emp_pin, emp_ssn, emp_firstname, emp_lastname, emp_phone, emp_photo, emp_privilege, emp_hiredate, emp_address, emp_active, emp_firedate, emp_firereason, emp_emergencyphone1, emp_emergencyphone2, emp_emergencyname, emp_emergencyaddress, emp_cardNumber, emp_country, emp_city, emp_state, emp_email, emp_title, emp_hourlyrate1, emp_hourlyrate2, emp_hourlyrate3, emp_hourlyrate4, emp_hourlyrate5, emp_gender, emp_birthday, emp_operationmode, emp_Line, emp_Passport, emp_MotobikeLicence, emp_CarLicence, IsSelect, middleware_id, nationalID, emp_Verify, emp_ViceCard, department_id, position_id FROM hr_employee LIMIT 10;'''
        data1 = cursorExternal.execute(sqlite_selet)

        connectionLocal.execute('''CREATE TABLE IF NOT EXISTS Student
         (id  integer primary key autoincrement, emp_pin TEXT not null, emp_ssn TEXT, emp_role TEXT)
         ''')

        # insert query
        for raw in data1:
            # print(raw)
            list_raw = list(raw)
            apend_list = [raw[3]+raw[4], raw[1] +
                          "@mail.com", "1234", True, False]
            list_raw.insert(
                1, (raw[3]+raw[4], raw[1] + "@mail.com", "1234", True, False))
            print(list_raw)
            # sqlite_insert = """INSERT INTO Student(id, full_name, email, hashed_password, is_active, is_superuser, emp_pin, emp_ssn, emp_firstname, emp_lastname, emp_phone, emp_photo, emp_privilege, emp_hiredate, emp_address, emp_active, emp_firedate, emp_firereason, emp_emergencyphone1, emp_emergencyphone2, emp_emergencyname, emp_emergencyaddress, emp_cardNumber, emp_country, emp_city, emp_state, emp_email, emp_title, emp_hourlyrate1, emp_hourlyrate2, emp_hourlyrate3, emp_hourlyrate4, emp_hourlyrate5, emp_gender, emp_birthday, emp_operationmode, emp_Line, emp_Passport, emp_MotobikeLicence, emp_CarLicence, IsSelect, middleware_id, nationalID, emp_Verify, emp_ViceCard, department_id, position_id)VALUES(?, ?, ?, ?)"""
        # using cursor object executing our query
            # cursorLocal.execute(sqlite_insert, raw)
            # connectionLocal.commit()
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
