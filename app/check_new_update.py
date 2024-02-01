import sqlite3
DATABASE_URL_EXTERNAL = "sqlite:///C:\\Users\\vieng\\OneDrive\\Private\\Xokthavi\\HR\\ZKTimeNet.db"
# DATABASE_URL_EXTERNAL = r"sqlite:///C:\Users\phuong\OneDrive\Private\Xokthavi\HR\ZKTimeNet.db"
DATABASE_URL_LOCAL = "sqlite:///./local.db"

print("===================",DATABASE_URL_EXTERNAL)
print("===================",DATABASE_URL_LOCAL)
# Connect to the databases
conn2 = sqlite3.connect(DATABASE_URL_LOCAL)
conn1 = sqlite3.connect(DATABASE_URL_EXTERNAL)

# Create cursor objects
cursor1 = conn1.cursor()
cursor2 = conn2.cursor()

# Retrieve data from tables
cursor1.execute("SELECT * FROM table1")
data1 = cursor1.fetchall()

cursor2.execute("SELECT * FROM table2")
data2 = cursor2.fetchall()
# (1, '0060', '0060', 'Miss Latsame', 'SITTHAKONE', '02078696545', None, '3', '2021-01-01 00:00:00', 'ບ້ານໜອງປິງ', 1, '2033-02-02 00:00:00', '', '02076736303', '', 'ທ ເຄືອ', 'ບ້ານໜອງປິງ', '0', "Lao People's Republic", 'ຈ່ັນທະບູລີ', 'ນະຄອນຫຼວງວຽງຈັນ', '', 'ບັນຊີ', 0, 0, 0, 0, 0, 1, '1995-11-23 00:00:00', 0, '', '', '', '', 0, 0, '', None, None, 2, 2)
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
