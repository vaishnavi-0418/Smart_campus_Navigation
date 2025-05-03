import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",               # ← your MySQL username
        password="root",   # ← your MySQL password
        database="smart_campus"    # ← your database name
    )