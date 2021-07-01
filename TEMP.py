import sqlite3

#start database conection
database = r"C:\Users\Jonathan\Personal OneDrive\OneDrive\GameDev\SaiBot\SaiDatabase.db"
dbconnection = sqlite3.connect(database)
cursor = dbconnection.cursor()

cursor.execute("DELETE FROM events")
cursor.execute("SELECT * FROM events")
print(cursor.fetchall())

#close database connection
dbconnection.commit()
dbconnection.close()
