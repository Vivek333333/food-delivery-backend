from mysql.connector import Error
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="66.116.229.214",
        user="a1784e1f_vivek",
        password="Vivek@512004",
        database="a1784e1f_mfd",
        port=3306
    )

def test_db_connection():
    try:
        conn = get_db()

        if conn.is_connected():
            print("✅ Database connected successfully!")
            print("MySQL Server Version:", conn.get_server_info())

            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db = cursor.fetchone()

            print("Connected Database:", db[0])

            cursor.close()

    except Error as e:
        print("❌ Connection failed!")
        print(e)

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Connection closed.")
