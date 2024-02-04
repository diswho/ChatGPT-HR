# https://www.geeksforgeeks.org/how-to-insert-image-in-sqlite-using-python/
import sqlite3
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_LOCAL = "sqlite:///./local.db"
# Function for Convert Binary Data
# to Human Readable Format

DATABASE_URL_EXTERNAL = 'SQLite_Retrieving_data.db'
DATABASE_URL_LOCAL = "sqlite:///./local.db"


def convertToBinaryData(filename):

    # Convert binary format to images
    # or files data
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertBLOB(name, photo):
    # query to create a table named FOOD1

    try:
        connectionLocal = sqlite3.connect(DATABASE_URL_EXTERNAL)
        cursorLocal = connectionLocal.cursor()

        connectionLocal.execute('''CREATE TABLE IF NOT EXISTS Student
         (name TEXT NOT NULL, img TEXT NOT NULL)
         ''')

        # insert query
        sqlite_insert_blob_query = """ 
            INSERT INTO Student 
            (name, img) 
            VALUES 
            (?, ?)"""
        data_tuple = (name, photo)

        # using cursor object executing our query
        cursorLocal.execute(sqlite_insert_blob_query, data_tuple)
        connectionLocal.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursorLocal.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if connectionLocal:
            connectionLocal.close()
            print("the sqlite connection is closed")


insertBLOB("Smith", "D:\Internship Tasks\GFG\images\One.png")
insertBLOB("David", "D:\Internship Tasks\GFG\images\person.png")
