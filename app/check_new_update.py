import sqlite3
DATABASE_URL_EXTERNAL = r"sqlite:///C:\\Users\\phuong\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

# Connect to the databases
conn1 = sqlite3.connect(DATABASE_URL_EXTERNAL)
conn2 = sqlite3.connect(DATABASE_URL_LOCAL)

# Create cursor objects
cursor1 = conn1.cursor()
cursor2 = conn2.cursor()

# Retrieve data from tables
cursor1.execute("SELECT * FROM table1")
data1 = cursor1.fetchall()

cursor2.execute("SELECT * FROM table2")
data2 = cursor2.fetchall()

# Compare data
for row1 in data1:
    # Check if row exists in table2
    if row1 not in data2:
        print("New Record found in table1:", row1)
    else:
        # Compare each field to identify updates
        index = data2.index(row1)
        for i in range(len(row1)):
            if row1[i] != data2[index][i]:
                print("Updated Record found:", row1, "->", data2[index])

# Close connections
conn1.close()
conn2.close()
