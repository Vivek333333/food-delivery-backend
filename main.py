from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error

app = FastAPI()


def get_db():
    return mysql.connector.connect(
        host="66.116.229.214",
        user="a1784e1f_vivek",
        password="Vivek@512004",
        database="a1784e1f_mfd",
        port=3306,
    )


@app.on_event("startup")
def startup_event():
    try:
        conn = get_db()

        if conn.is_connected():
            print("✅ Database connected successfully!")
            print("MySQL Version:", conn.get_server_info())

            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db = cursor.fetchone()

            print("Database:", db[0])

            cursor.close()
            conn.close()

    except Error as e:
        print("❌ Database connection failed:")
        print(e)
