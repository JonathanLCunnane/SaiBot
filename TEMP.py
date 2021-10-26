import sqlite3

#start database conection
database = r".\SaiDatabase.db"
dbconnection = sqlite3.connect(database)
cursor = dbconnection.cursor()

cursor.execute(""" SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME="saisupportstats" """)
print(cursor.fetchall())

#close database connection
dbconnection.commit()
dbconnection.close()