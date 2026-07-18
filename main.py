from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel
from typing import List, Optional, Dict
import random
import os
import requests
from mysql.connector import Error

app = FastAPI()

# Enable CORS so your React Expo app can make requests to this backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make uploads folder public
app.mount("/images", StaticFiles(directory="images"), name="images")

# Dynamic IP string used for formatting your media assets securely
BASE_MEDIA_URL = "http://192.168.1.6:8000/images/"

# Global in-memory storage for OTPs (Key: phone number, Value: dict with OTP and expiry time)
otp_store: Dict[str, dict] = {}

def get_db():
    return mysql.connector.connect(
        host="66.116.229.214", user="a1784e1f_vivek", password="Vivek@512004", database="a1784e1f_mfd",port=3306
    )

# ---------------- SMS DISPATCH UTILITY ----------------
 if conn.is_connected():
        print("✅ Database connected successfully!")
        print("MySQL Server Version:", conn.get_server_info())

        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print("Connected Database:", db[0])

except Error as e:
    print("❌ Connection failed!")
    print(e)

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed.")
