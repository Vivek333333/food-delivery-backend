from datetime import datetime, timedelta
import os
import random
import shutil
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
import requests

# Initialize Directories
IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

app = FastAPI(title="Unified Restaurant System & Admin API")

# Enable CORS for frontend clients (React Native / Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve stored images statically
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

# Media base URL configuration
BASE_MEDIA_URL = "https://johnmarcos.online/images/"

# In-memory OTP storage
otp_store: Dict[str, dict] = {}


# ---------------- DATABASE CONFIGURATION ----------------
def get_db():
    """Database connection factory used across all routes."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mfd",
    )


def init_db():
    """Initializes required database tables on startup if they do not exist."""
    conn = get_db()
    cursor = conn.cursor()

    # User Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `user` (
            uid INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            phone VARCHAR(50) NOT NULL
        )
    """)

    # Restaurants Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            rid INT AUTO_INCREMENT PRIMARY KEY,
            rname VARCHAR(255) NOT NULL,
            images VARCHAR(255) NOT NULL
        )
    """)

    # Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            pid INT AUTO_INCREMENT PRIMARY KEY,
            rid INT NOT NULL,
            product VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            images VARCHAR(255) NOT NULL,
            FOREIGN KEY (rid) REFERENCES restaurants (rid) ON DELETE CASCADE
        )
    """)

    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            oid INT AUTO_INCREMENT PRIMARY KEY,
            pid INT NOT NULL,
            uid INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL,
            address TEXT NOT NULL,
            paymenttype VARCHAR(100) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'preparing',
            FOREIGN KEY (pid) REFERENCES products (pid) ON DELETE CASCADE,
            FOREIGN KEY (uid) REFERENCES `user` (uid) ON DELETE CASCADE
        )
    """)

    # Cart Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            uid INT,
            pid INT,
            PRIMARY KEY (uid, pid),
            FOREIGN KEY (uid) REFERENCES `user` (uid) ON DELETE CASCADE,
            FOREIGN KEY (pid) REFERENCES products (pid) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# Initialize table schema
init_db()


# ---------------- HELPER FUNCTIONS ----------------
def send_otp_via_fast2sms(phone: str, otp: str):
    api_key = os.getenv(
        "FAST2SMS_API_KEY",
        "nSSzfhIWmF3Z876lTgJA2QznUUtH7qWE1MZiv1wGQKpDJDe5Od7mFmCRaKzD",
    )
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {"authorization": api_key, "Content-Type": "application/json"}
    payload = {
        "variables_values": otp,
        "route": "otp",
        "numbers": phone,
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(
            f"Fast2SMS response: status {response.status_code}, payload {response.text}"
        )
    except Exception as e:
        print(f"Fast2SMS notification failure: {e}")


# ---------------- SCHEMAS ----------------
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
    quantity: Optional[int] = 1


class OrderItemResponse(BaseModel):
    pid: int
    rid: Optional[int] = None
    restaurant_name: Optional[str] = None
    product: str
    price: float
    image: str
    address: str
    quantity: int
    total_amount: float
    paymenttype: str
    status: str


class PlaceOrder(BaseModel):
    uid: int
    address: str
    paymenttype: str
    items: List[OrderItem]


class OrderStatusUpdate(BaseModel):
    status: str


# ---------------- SYSTEM / HEALTH ENDPOINTS ----------------
@app.get("/")
@app.get("/db-test")
def home():
    conn = None
    try:
        conn = get_db()
        if conn.is_connected():
            return {
                "message": "FastAPI System Operating Normally",
                "database": "Database connection verified",
            }
        return {
            "message": "FastAPI Operating",
            "database": "Connection offline",
        }
    except Error as e:
        return {"message": "FastAPI Operating", "database": str(e)}
    finally:
        if conn and conn.is_connected():
            conn.close()


@app.get("/delete-account", response_class=HTMLResponse)
def delete_account():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Delete Account</title>
    </head>
    <body style="font-family: Arial; margin:40px;">
        <h1>Delete Your Account</h1>
        <p>If you want to delete your account, please send an email with your registered phone number.</p>
        <h3>Steps to Delete Your Account</h3>
        <ol>
            <li>Send an email with your registered phone number.</li>
            <li>We will verify your request.</li>
            <li>Your account will be permanently deleted within 7 days.</li>
        </ol>
        <h3>Data Deleted</h3>
        <ul>
            <li>User Profile</li>
            <li>Orders</li>
            <li>Cart</li>
            <li>Saved Addresses</li>
        </ul>
        <h3>Data Retained</h3>
        <p>No personal data is retained except where required by law.</p>
        <p>Email: <b>johnmarcospizza@gmail.com</b></p>
    </body>
    </html>
    """


# ---------------- AUTHENTICATION ROUTES ----------------
@app.post("/register")
def register(user: Register):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM user WHERE phone=%s", (user.phone,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=400, detail="Phone number already exists"
            )

        cursor.execute(
            "INSERT INTO user (username, phone) VALUES (%s, %s)",
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
            raise HTTPException(
                status_code=404, detail="User account not found"
            )

        generated_otp = str(random.randint(100000, 999999))
        otp_store[payload.phone] = {
            "otp": generated_otp,
            "expires_at": datetime.now() + timedelta(minutes=5),
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
            raise HTTPException(
                status_code=404, detail="User profile mismatch"
            )

        stored_data = otp_store.get(payload.phone)

        if (
            not stored_data
            or datetime.now() > stored_data["expires_at"]
            or stored_data["otp"] != payload.otp
            or payload.otp == ""
        ):
            raise HTTPException(
                status_code=401, detail="Invalid or expired OTP"
            )

        if payload.phone in otp_store:
            del otp_store[payload.phone]

        return {
            "success": True,
            "message": "Successful login",
            "user": {
                "uid": db_user["uid"],
                "username": db_user["username"],
                "phone": db_user["phone"],
            },
        }
    finally:
        cursor.close()
        db.close()


# ---------------- RESTAURANT ENDPOINTS ----------------
@app.get("/restaurants")
@app.get("/uploads")
@app.get("/api/restaurants")
def get_restaurants():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT rid, rname, rname AS restaurants, images FROM restaurants"
        )
        rows = cursor.fetchall()
        for row in rows:
            if row.get("images"):
                row["images"] = f"{BASE_MEDIA_URL}{row['images']}"
        return rows
    finally:
        cursor.close()
        db.close()


@app.get("/restaurants/{rid}/products")
def get_restaurant_products(rid: int):
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


@app.post("/uploads")
async def upload_restaurant(
    restaurants: str = Form(...), file: UploadFile = File(...)
):
    saved_filename = file.filename
    file_path = os.path.join(IMAGES_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    conn = get_db()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO restaurants (rname, images) VALUES (%s, %s)"
        cursor.execute(sql, (restaurants, saved_filename))
        conn.commit()
        return {"message": "Image uploaded", "path": saved_filename}
    finally:
        cursor.close()
        conn.close()


@app.delete("/delete_restaurant/{rid}")
@app.delete("/api/restaurants/{rid}")
async def delete_restaurant(rid: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT images FROM restaurants WHERE rid = %s", (rid,)
        )
        row = cursor.fetchone()
        if row and row["images"]:
            img_path = os.path.join(
                IMAGES_DIR, os.path.basename(row["images"])
            )
            if os.path.exists(img_path):
                os.remove(img_path)

        cursor.execute("DELETE FROM restaurants WHERE rid = %s", (rid,))
        conn.commit()
        return {"status": "success", "deleted": rid}
    finally:
        cursor.close()
        conn.close()


# ---------------- PRODUCT ENDPOINTS ----------------
@app.post("/api/products")
async def add_product(
    rid: int = Form(...),
    product: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT rid FROM restaurants WHERE rid = %s", (rid,))
        restaurant = cursor.fetchone()
        if not restaurant:
            raise HTTPException(
                status_code=400,
                detail="Associated Restaurant ID does not exist",
            )

        file_extension = os.path.splitext(image.filename)[1]
        saved_filename = (
            f"product_{int(os.urandom(4).hex(), 16)}{file_extension}"
        )
        file_path = os.path.join(IMAGES_DIR, saved_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        cursor.execute(
            "INSERT INTO products (rid, product, price, images) VALUES (%s, %s, %s, %s)",
            (rid, product, price, saved_filename),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return {"status": "success", "pid": new_id, "images": saved_filename}
    finally:
        cursor.close()
        conn.close()


@app.get("/products")
@app.get("/api/products")
async def list_products():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT p.pid, p.rid, p.product, p.product AS pname, p.price, p.images,
                   r.rname AS restaurant_name
            FROM products p
            LEFT JOIN restaurants r ON p.rid = r.rid
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            if row.get("images"):
                row["images"] = f"{BASE_MEDIA_URL}{row['images']}"
        return rows
    finally:
        cursor.close()
        conn.close()


@app.delete("/delete_product/{pid}")
@app.delete("/api/products/{pid}")
async def delete_product(pid: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT images FROM products WHERE pid = %s", (pid,))
        row = cursor.fetchone()
        if row and row["images"]:
            img_path = os.path.join(
                IMAGES_DIR, os.path.basename(row["images"])
            )
            if os.path.exists(img_path):
                os.remove(img_path)

        cursor.execute("DELETE FROM products WHERE pid = %s", (pid,))
        conn.commit()
        return {"status": "success", "deleted": pid}
    finally:
        cursor.close()
        conn.close()


# ---------------- CART ENDPOINTS ----------------
@app.post("/add-cart")
def add_cart(data: Cart):
    db = get_db()
    cursor = db.cursor()
    try:
        sql = "INSERT INTO cart (uid, pid) VALUES (%s, %s)"
        cursor.execute(sql, (data.uid, data.pid))
        db.commit()
        return {"success": True, "message": "Added to cart"}
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
            "DELETE FROM cart WHERE uid=%s AND pid=%s", (uid, pid)
        )
        db.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Item not found"}

        return {"success": True, "message": "Item removed from cart"}
    finally:
        cursor.close()
        db.close()


# ---------------- ORDER ENDPOINTS ----------------
@app.post("/place-order")
def place_order(order_data: PlaceOrder):
    db = get_db()
    cursor = db.cursor()
    try:
        if not order_data.items:
            raise HTTPException(
                status_code=400, detail="No items found in order payload"
            )

        if not order_data.address or not order_data.address.strip():
            raise HTTPException(
                status_code=400, detail="Delivery address cannot be empty"
            )

        insert_query = """
        INSERT INTO `orders` (pid, uid, price, quantity, address, paymenttype, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'preparing')
        """

        for item in order_data.items:
            qty = item.quantity if (item.quantity and item.quantity > 0) else 1
            cursor.execute(
                insert_query,
                (
                    item.pid,
                    order_data.uid,
                    item.price,
                    qty,
                    order_data.address.strip(),
                    order_data.paymenttype.strip(),
                ),
            )

        cursor.execute("DELETE FROM cart WHERE uid = %s", (order_data.uid,))
        db.commit()
        return {
            "success": True,
            "message": "Your purchase records have been submitted!",
        }

    except Error as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Database transaction processing failure"
        )
    finally:
        cursor.close()
        db.close()


@app.get("/orders/{uid}", response_model=List[OrderItemResponse])
def get_user_orders(uid: int):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                o.pid, 
                p.rid,
                COALESCE(r.rname, 'Unknown Restaurant') AS restaurant_name,
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
            LEFT JOIN restaurants r ON p.rid = r.rid
            WHERE o.uid = %s
            GROUP BY o.pid, p.rid, r.rname, p.product, p.price, p.images, o.address, o.paymenttype, o.status
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


@app.get("/orders")
@app.get("/api/orders")
async def list_orders():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                o.oid, 
                o.pid, 
                p.rid,
                COALESCE(r.rname, 'Unknown Restaurant') AS restaurant_name,
                o.uid, 
                COALESCE(p.product, 'Unknown Product') AS product_name,
                COALESCE(u.username, 'Unknown User') AS username,
                COALESCE(u.phone, 'N/A') AS mobile,
                o.price, 
                o.quantity, 
                o.address, 
                o.paymenttype, 
                o.status
            FROM orders o
            LEFT JOIN products p ON o.pid = p.pid
            LEFT JOIN restaurants r ON p.rid = r.rid
            LEFT JOIN `user` u ON o.uid = u.uid
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


@app.put("/api/orders/{oid}/status")
async def update_order_status(oid: int, status_update: OrderStatusUpdate):
    valid_statuses = ["preparing", "on the way", "delivered"]
    if status_update.status.lower() not in valid_statuses:
        raise HTTPException(
            status_code=400, detail="Invalid status assignment"
        )

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE orders SET status = %s WHERE oid = %s",
            (status_update.status.lower(), oid),
        )
        conn.commit()
        return {
            "status": "success",
            "updated_oid": oid,
            "new_status": status_update.status,
        }
    finally:
        cursor.close()
        conn.close()


@app.delete("/orders/remove/{uid}/{pid}")
def remove_order_item(uid: int, pid: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM `orders` WHERE uid=%s AND pid=%s", (uid, pid)
        )
        db.commit()

        if cursor.rowcount == 0:
            return {"success": False, "message": "Order entry not found"}

        return {"success": True, "message": "Order entry completely removed"}
    finally:
        cursor.close()
        db.close()


@app.delete("/api/orders/{oid}")
async def delete_order(oid: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE oid = %s", (oid,))
        conn.commit()
        return {"status": "success", "deleted": oid}
    finally:
        cursor.close()
        conn.close()


# ---------------- USER MANAGEMENT ENDPOINTS ----------------
@app.get("/users")
@app.get("/api/users")
async def list_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT uid, username, phone, phone AS mobile FROM `user`"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


@app.delete("/delete_user/{uid}")
@app.delete("/api/users/{uid}")
async def delete_user(uid: int):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cart WHERE uid = %s", (uid,))
        cursor.execute("DELETE FROM orders WHERE uid = %s", (uid,))
        cursor.execute("DELETE FROM `user` WHERE uid = %s", (uid,))
        conn.commit()
        return {"status": "success", "deleted": uid}
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
