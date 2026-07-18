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


@app.get("/")
def home():
    return {"message": "FastAPI is running"}


@app.get("/db-test")
def db_test():
    try:
        conn = get_db()

        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db = cursor.fetchone()[0]

            version = conn.get_server_info()

            cursor.close()
            conn.close()

            return {
                "success": True,
                "message": "Database connected successfully",
                "database": db,
                "mysql_version": version,
            }

    except Error as e:
        return {
            "success": False,
            "message": str(e),
        }
