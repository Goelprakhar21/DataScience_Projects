import sqlite3

#connecting to sqlite usign python
connection=sqlite3.connect('Countries.db')

#Creating a cursor to create records, read records, create table, insert records and other operations
cursor = connection.cursor()

#Creating a table named Countries
table_info="""
Create table COUNTRIES(NAME VARCHAR(25), CAPITAL VARCHAR(25), CURRENCY VARCHAR(25), PHONECODE INT);

"""
cursor.execute(table_info)

#Inserting records into the table

cursor.execute("""Insert into COUNTRIES values("India", "New Delhi","INR",91) """)
cursor.execute("""Insert into COUNTRIES values("Afghanistan", "Kabul","AFN",93) """)
cursor.execute("""Insert into COUNTRIES values("Albania", "Tirana","ALL",35) """)
cursor.execute("""Insert into COUNTRIES values("Austria", "Vienna","EUR",43) """)
cursor.execute("""Insert into COUNTRIES values("Bangladesh", "Dhaka","BDT",880) """)
cursor.execute("""Insert into COUNTRIES values("Australia", "Canberra","AUD",61) """)
cursor.execute("""Insert into COUNTRIES values("Netherlands", "Amsterdam","ANG",20) """)
cursor.execute("""Insert into COUNTRIES values("England", "London","GBP",44) """)
cursor.execute("""Insert into COUNTRIES values("Ecuador", "Quito","USD",593) """)
cursor.execute("""Insert into COUNTRIES values("USA", "Washington DC","USD",1) """)

## Displaying the records that are inserted
print("The inserted records are")
data = cursor.execute('''Select * from COUNTRIES''')

for row in data:
    print(row)

#Closing the SQL Connection

connection.commit()
connection.close()

