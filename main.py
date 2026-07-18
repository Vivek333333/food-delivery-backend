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
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com", user="3ASVq3fvFfmEeAQ.root", password="pFLo80lCth6C9gx5", database="a1784e1f_mfd"
    )

# ---------------- SMS DISPATCH UTILITY ----------------
def send_otp_via_fast2sms(phone: str, otp: str):
    api_key = os.getenv("FAST2SMS_API_KEY","nSSzfhIWmF3Z876lTgJA2QznUUtH7qWE1MZiv1wGQKpDJDe5Od7mFmCRaKzD")
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        'authorization': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'variables_values': otp,
        'route': 'otp',
        'numbers': phone,
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Fast2SMS API response status: {response.status_code}, response: {response.text}")
    except Exception as e:
        print(f"Network error trying to hit Fast2SMS: {e}")

# ---------------- PYDANTIC SCHEMAS ----------------
class Register(BaseModel):
    username: str
    phone: str

class SendOTP(BaseModel):
    phone: str

class VerifyOTP(BaseModel):
    phone: str
    otp: str

class Cart(BaseModel):
    uid: int
    pid: int

class CartItemResponse(BaseModel):
    pid: int
    rid: int
    product: str
    price: float
    image: str

class OrderItem(BaseModel):
    pid: int
    price: float
    quantity: Optional[int] = 1  # Default to 1 if the client doesn't send a quantity

# Added 'status' and corrected 'paymenttype' in the response schema
class OrderItemResponse(BaseModel):
    pid: int
    product: str
    price: float
    image: str
    address: str
    quantity: int
    total_amount: float
    paymenttype: str
    status: str

# Corrected 'paymenttype' in the incoming payload schema
class PlaceOrder(BaseModel):
    uid: int
    address: str  
    paymenttype: str  
    items: List[OrderItem]

# ---------------- RESTAURANTS ROUTES ----------------
@app.get("/restaurants")
def get_restaurants():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM restaurants")
        rows = cursor.fetchall()
        for row in rows:
            if row.get("images"):
                row["images"] = f"{BASE_MEDIA_URL}{row['images']}"
        return rows
    finally:
        cursor.close()
        db.close()

@app.get("/restaurants/{rid}/products")
def restaurant_products(rid: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM products WHERE rid=%s", (rid,))
        datas = cursor.fetchall()
        for data in datas:
            if data.get("images"):
                data["images"] = f"{BASE_MEDIA_URL}{data['images']}"
        return datas
    finally:
        cursor.close()
        db.close()

# ---------------- AUTH ROUTES ----------------
@app.post("/register")
def register(user: Register):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM user WHERE phone=%s", (user.phone,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Phone number already exists")

        cursor.execute(
            """
            INSERT INTO user (username, phone)
            VALUES (%s, %s)
            """,
            (user.username, user.phone),
        )
        db.commit()
        return {"success": True, "message": "Registration Successful"}
    finally:
        cursor.close()
        db.close()

@app.post("/send-otp")
def send_otp(payload: SendOTP):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user WHERE phone=%s", (payload.phone,))
        db_user = cursor.fetchone()
        if not db_user:
            raise HTTPException(status_code=404, detail="User account not found with this number")

        generated_otp = str(random.randint(100000, 999999))
        
        otp_store[payload.phone] = {
            "otp": generated_otp,
            "expires_at": datetime.now() + timedelta(minutes=5)
        }

        send_otp_via_fast2sms(payload.phone, generated_otp)

        return {"success": True, "message": "OTP Sent Successfully"}
    finally:
        cursor.close()
        db.close()

@app.post("/login-verify")
def login_verify(payload: VerifyOTP):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user WHERE phone=%s", (payload.phone,))
        db_user = cursor.fetchone()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User profile mismatch")

        stored_data = otp_store.get(payload.phone)

        if (
            not stored_data 
            or datetime.now() > stored_data["expires_at"] 
            or stored_data["otp"] != payload.otp 
            or payload.otp == ""
        ):
            raise HTTPException(status_code=401, detail="please try again")

        if payload.phone in otp_store:
            del otp_store[payload.phone]

        return {
            "success": True,
            "message": "Successful login",
            "user": {
                "uid": db_user["uid"],
                "username": db_user["username"],
                "phone": db_user["phone"]
            },
        }
    finally:
        cursor.close()
        db.close()

# ---------------- CART ROUTES ----------------
@app.post("/add-cart")
def addcart(data: Cart):
    db = get_db()
    cursor = db.cursor()
    try:
        sql = """
        INSERT INTO cart (uid, pid)
        VALUES (%s, %s)
        """
        cursor.execute(sql, (data.uid, data.pid))
        db.commit()
        return {"success": True, "message": "Added"}
    finally:
        cursor.close()
        db.close()

@app.get("/cart/{uid}", response_model=List[CartItemResponse])
def get_user_cart(uid: int):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT p.pid, p.rid, p.product, p.price, p.images 
            FROM cart c
            JOIN products p ON c.pid = p.pid
            WHERE c.uid = %s
        """
        cursor.execute(query, (uid,))
        results = cursor.fetchall()
        
        for row in results:
            if row.get("images"):
                row["image"] = f"{BASE_MEDIA_URL}{row['images']}"
                del row["images"]
            else:
                row["image"] = "https://via.placeholder.com/100"
                
        return results
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@app.delete("/cart/remove/{uid}/{pid}")
def remove_cart(uid: int, pid: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM cart WHERE uid=%s AND pid=%s",
            (uid, pid)
        )
        db.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Item not found"}

        return {"success": True, "message": "Item removed"}
    finally:
        cursor.close()
        db.close()

# ---------------- ORDER ROUTES ----------------
@app.post("/place-order")
def place_order(order_data: PlaceOrder):
    db = get_db()
    cursor = db.cursor()
    try:
        if not order_data.items:
            raise HTTPException(status_code=400, detail="No items found in the order request")

        if not order_data.address or not order_data.address.strip():
            raise HTTPException(status_code=400, detail="Delivery address cannot be empty")

        # FIX: Included 'quantity' explicitly in the column mapping and insert values
        insert_query = """
        INSERT INTO `orders` (pid, uid, price, quantity, address, paymenttype, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
        """

        for item in order_data.items:
            # Enforce dynamic fallback fallback to 1 if no quantity is provided
            qty = item.quantity if (item.quantity and item.quantity > 0) else 1
            
            cursor.execute(
                insert_query,
                (
                    item.pid, 
                    order_data.uid, 
                    item.price, 
                    qty,
                    order_data.address.strip(), 
                    order_data.paymenttype.strip()
                )
            )

        # Clean cart state for the user upon order finalization
        cursor.execute("DELETE FROM cart WHERE uid = %s", (order_data.uid,))
        db.commit()
        return {"success": True, "message": "Your purchase records have been submitted!"}
        
    except Error as e:
        db.rollback()
        print("SQL Error processing final checkout:", e)
        raise HTTPException(status_code=500, detail="Database transaction processing failure")
    finally:
        cursor.close()
        db.close()

@app.get("/orders/{uid}", response_model=List[OrderItemResponse])
def get_user_orders(uid: int):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    try:
        # FIX: Grouped and summed 'quantity' explicitly, calculating total item cost by multiplying price * quantity
        query = """
            SELECT 
                o.pid, 
                p.product, 
                p.price, 
                p.images, 
                o.address,
                o.paymenttype,
                o.status,
                SUM(o.quantity) as quantity,
                SUM(o.price * o.quantity) as total_amount
            FROM `orders` o
            JOIN products p ON o.pid = p.pid
            WHERE o.uid = %s
            GROUP BY o.pid, p.product, p.price, p.images, o.address, o.paymenttype, o.status
        """
        cursor.execute(query, (uid,))
        results = cursor.fetchall()
        
        for row in results:
            if row.get("images"):
                row["image"] = f"{BASE_MEDIA_URL}{row['images']}"
                del row["images"]
            else:
                row["image"] = "https://via.placeholder.com/100"
                
        return results
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@app.delete("/orders/remove/{uid}/{pid}")
def remove_order(uid: int, pid: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM `orders` WHERE uid=%s AND pid=%s",
            (uid, pid)
        )
        db.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Order entry not found"}

        return {"success": True, "message": "Order entry completely removed"}
    finally:
        cursor.close()
        db.close()
