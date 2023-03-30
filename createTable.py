from tkinter import messagebox as msg
import sqlite3 as db

try:
    conn = db.connect('myDb.db')
    print("Connection Established: Connected to myDb Database!")
    cursor = conn.cursor()
except db.DatabaseError:
    print(db.DatabaseError)

def createTable():
    with conn:
        cursor.execute("""CREATE TABLE IF NOT EXISTS PRODUCT (
                            PRODUCT_ID INTEGER PRIMARY KEY,
                            PRODUCT_CATEGORY VARCHAR(20),
                            PRODUCT_NAME VARCHAR(20),
                            PRODUCT_BRAND VARCHAR(20)
                            );""")
        msg.showinfo("CREATE TABLE", "Table Created Successfully!")

createTable()