import os
import random
import uuid
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import mysql.connector
from mysql.connector import Error

from pydantic import BaseModel


# =========================================================
# CONFIGURATION
# =========================================================

IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

app = FastAPI(
    title="Unified Restaurant System & Admin API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# STATIC IMAGES & SERVER IP
# =========================================================

app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
BASE_MEDIA_URL = "https://johnmarcos.online/images/"


# =========================================================
# OTP STORAGE
# =========================================================

otp_store: Dict[str, dict] = {}


# =========================================================
# DATABASE
# =========================================================

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mfd",
    )


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `user` (
                uid INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                phone VARCHAR(50) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                rid INT AUTO_INCREMENT PRIMARY KEY,
                rname VARCHAR(255) NOT NULL,
                images VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                catid INT AUTO_INCREMENT PRIMARY KEY,
                rid INT NOT NULL,
                cat VARCHAR(255) NOT NULL,
                images VARCHAR(255) NOT NULL,
                CONSTRAINT fk_category_restaurant
                FOREIGN KEY (rid)
                REFERENCES restaurants(rid)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                pid INT AUTO_INCREMENT PRIMARY KEY,
                rid INT NOT NULL,
                catid INT NOT NULL,
                product VARCHAR(255) NOT NULL,
                images VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                CONSTRAINT fk_product_restaurant
                FOREIGN KEY (rid)
                REFERENCES restaurants(rid)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
                CONSTRAINT fk_product_category
                FOREIGN KEY (catid)
                REFERENCES category(catid)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                oid INT AUTO_INCREMENT PRIMARY KEY,
                pid INT NOT NULL,
                uid INT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                quantity INT NOT NULL,
                address TEXT NOT NULL,
                paymenttype VARCHAR(100) NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'pending',
                FOREIGN KEY (pid)
                REFERENCES products(pid)
                ON DELETE CASCADE,
                FOREIGN KEY (uid)
                REFERENCES `user`(uid)
                ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                uid INT,
                pid INT,
                PRIMARY KEY(uid, pid),
                FOREIGN KEY(uid)
                REFERENCES `user`(uid)
                ON DELETE CASCADE,
                FOREIGN KEY(pid)
                REFERENCES products(pid)
                ON DELETE CASCADE
            )
        """)

        conn.commit()

    finally:
        cursor.close()
        conn.close()


init_db()


# =========================================================
# HELPERS
# =========================================================

def attach_image_url(row: dict, key: str = "images") -> dict:
    if row.get(key):
        filename = str(row[key])
        if filename.startswith("http://") or filename.startswith("https://"):
            return row
        filename = os.path.basename(filename)
        row[key] = f"{BASE_MEDIA_URL}{filename}"
    return row


def save_uploaded_file(upload_file: UploadFile, prefix: str):
    extension = os.path.splitext(upload_file.filename or "")[1]
    if not extension:
        extension = ".jpg"
    filename = f"{prefix}_{uuid.uuid4().hex}{extension}"
    path = os.path.join(IMAGES_DIR, filename)
    return filename, path


def send_otp_via_fast2sms(phone: str, otp: str):
    api_key = os.getenv(
        "FAST2SMS_API_KEY",
        "nSSzfhIWmF3Z876lTgJA2QznUUtH7qWE1MZiv1wGQKpDJDe5Od7mFmCRaKzD"
    )
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "variables_values": otp,
        "route": "otp",
        "numbers": phone,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print("Fast2SMS response:", response.status_code, response.text)
    except Exception as e:
        print("Fast2SMS notification failure:", e)


# =========================================================
# PYDANTIC MODELS
# =========================================================

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
    oid: Optional[int] = None
    pid: int
    uid: int
    username: Optional[str] = "Unknown User"
    phone: Optional[str] = None
    product: str
    price: float
    quantity: int
    address: str
    paymenttype: str
    status: str
    image: Optional[str] = None


class PlaceOrder(BaseModel):
    uid: int
    address: str
    paymenttype: str
    items: List[OrderItem]


class OrderStatusUpdate(BaseModel):
    status: str


class ProductResponse(BaseModel):
    pid: int
    rid: int
    catid: int
    product: str
    price: float
    images: str
    restaurant_name: Optional[str] = None
    category_name: Optional[str] = None


# =========================================================
# HOME / DATABASE TEST
# =========================================================

@app.get("/")
@app.get("/db-test")
def home():
    conn = None
    try:
        conn = get_db()
        if conn.is_connected():
            return {
                "message": "FastAPI System Operating Normally",
                "database": "Database connection verified"
            }
        return {
            "message": "FastAPI Operating",
            "database": "Connection offline"
        }
    except Error as e:
        return {
            "message": "FastAPI Operating",
            "database": str(e)
        }
    finally:
        if conn and conn.is_connected():
            conn.close()


# =========================================================
# DELETE ACCOUNT PAGE
# =========================================================

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


# =========================================================
# AUTHENTICATION
# =========================================================

@app.post("/register")
def register(user: Register):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM `user` WHERE phone=%s", (user.phone,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Phone number already exists")

        cursor.execute(
            "INSERT INTO `user` (username, phone) VALUES (%s, %s)",
            (user.username, user.phone)
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
        cursor.execute("SELECT * FROM `user` WHERE phone=%s", (payload.phone,))
        db_user = cursor.fetchone()
        if not db_user:
            raise HTTPException(status_code=404, detail="User account not found")

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
        cursor.execute("SELECT * FROM `user` WHERE phone=%s", (payload.phone,))
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
            raise HTTPException(status_code=401, detail="Invalid or expired OTP")

        otp_store.pop(payload.phone, None)
        return {
            "success": True,
            "message": "Successful login",
            "user": {
                "uid": db_user["uid"],
                "username": db_user["username"],
                "phone": db_user["phone"],
            }
        }
    finally:
        cursor.close()
        db.close()


# =========================================================
# RESTAURANT HIERARCHY
# =========================================================

@app.get("/api/restaurant-hierarchy")
def get_restaurant_hierarchy(rid: Optional[int] = Query(None)):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        restaurant_query = "SELECT rid, rname, images FROM restaurants"
        restaurant_params = []

        if rid is not None:
            restaurant_query += " WHERE rid=%s"
            restaurant_params.append(rid)

        # Newest restaurant should appear LAST in the list
        restaurant_query += " ORDER BY rid ASC"

        cursor.execute(restaurant_query, tuple(restaurant_params))
        restaurants = cursor.fetchall()

        if not restaurants:
            return []

        restaurant_ids = [restaurant["rid"] for restaurant in restaurants]
        placeholders = ",".join(["%s"] * len(restaurant_ids))

        # Newest category should appear LAST in the list
        category_query = f"""
            SELECT catid, rid, cat, images
            FROM category
            WHERE rid IN ({placeholders})
            ORDER BY catid ASC
        """
        cursor.execute(category_query, tuple(restaurant_ids))
        categories = cursor.fetchall()

        # Newest product should appear LAST in the list
        product_query = f"""
            SELECT p.pid, p.rid, p.catid, p.product, p.images, p.price
            FROM products p
            INNER JOIN category c ON p.catid = c.catid AND p.rid = c.rid
            WHERE p.rid IN ({placeholders})
            ORDER BY p.pid ASC
        """
        cursor.execute(product_query, tuple(restaurant_ids))
        products = cursor.fetchall()

        products_map = {}
        for product in products:
            attach_image_url(product)
            if product.get("price") is not None:
                product["price"] = float(product["price"])
            key = (product["rid"], product["catid"])
            if key not in products_map:
                products_map[key] = []
            products_map[key].append(product)

        categories_map = {}
        for category in categories:
            attach_image_url(category)
            key = (category["rid"], category["catid"])
            category["products"] = products_map.get(key, [])
            if category["rid"] not in categories_map:
                categories_map[category["rid"]] = []
            categories_map[category["rid"]].append(category)

        result = []
        for restaurant in restaurants:
            attach_image_url(restaurant)
            restaurant["categories"] = categories_map.get(restaurant["rid"], [])
            result.append(restaurant)

        return result

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()


# =========================================================
# CATEGORIES
# =========================================================

@app.post("/add-category")
@app.post("/api/category")
async def add_category(
    rid: int = Form(...),
    cat: str = Form(...),
    images: UploadFile = File(...)
):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT rid FROM restaurants WHERE rid=%s", (rid,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Restaurant not found")

        saved_filename, file_path = save_uploaded_file(images, "cat")
        content = await images.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        cursor.execute(
            "INSERT INTO category (rid, cat, images) VALUES (%s, %s, %s)",
            (rid, cat, saved_filename)
        )
        conn.commit()

        return {
            "success": True,
            "message": "Category added successfully",
            "catid": cursor.lastrowid,
            "rid": rid,
            "cat": cat,
            "images": f"{BASE_MEDIA_URL}{saved_filename}"
        }
    finally:
        cursor.close()
        conn.close()


@app.get("/category")
@app.get("/api/category")
def get_categories(rid: Optional[int] = Query(None)):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT catid, rid, cat, images FROM category"
        params = []
        if rid is not None:
            query += " WHERE rid=%s"
            params.append(rid)
        # Newest category should appear LAST in the list
        query += " ORDER BY catid ASC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [attach_image_url(row) for row in rows]
    finally:
        cursor.close()
        db.close()


@app.get("/restaurants/{rid}/categories")
def get_restaurant_categories(rid: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            # Newest category should appear LAST in the list
            "SELECT catid, rid, cat, images FROM category WHERE rid=%s ORDER BY catid ASC",
            (rid,)
        )
        rows = cursor.fetchall()
        return [attach_image_url(row) for row in rows]
    finally:
        cursor.close()
        db.close()


@app.get("/api/restaurants/{rid}/categories-with-details")
def get_categories_with_restaurant_details(rid: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.catid, c.rid, c.cat, c.images, r.rname AS restaurant_name
            FROM category c
            INNER JOIN restaurants r ON c.rid = r.rid
            WHERE c.rid=%s
            ORDER BY c.catid ASC
        """, (rid,))
        rows = cursor.fetchall()
        return [attach_image_url(row) for row in rows]
    finally:
        cursor.close()
        db.close()


@app.delete("/delete_category/{cid}")
@app.delete("/api/category/{cid}")
async def delete_category(cid: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT images FROM category WHERE catid=%s", (cid,))
        row = cursor.fetchone()
        if row and row["images"]:
            path = os.path.join(IMAGES_DIR, os.path.basename(row["images"]))
            if os.path.exists(path):
                os.remove(path)

        cursor.execute("DELETE FROM category WHERE catid=%s", (cid,))
        conn.commit()
        return {"status": "success", "deleted": cid}
    finally:
        cursor.close()
        conn.close()


# =========================================================
# RESTAURANTS
# =========================================================

@app.get("/restaurants")
@app.get("/uploads")
@app.get("/api/restaurants")
def get_restaurants():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT rid, rname, rname AS restaurants, images
            FROM restaurants
            ORDER BY rid ASC
        """)
        rows = cursor.fetchall()
        return [attach_image_url(row) for row in rows]
    finally:
        cursor.close()
        db.close()


@app.get("/restaurants/{rid}/products")
def get_restaurant_products(rid: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.pid, p.rid, p.catid, p.product, p.images, p.price, c.cat AS category_name
            FROM products p
            INNER JOIN category c ON p.catid = c.catid AND p.rid = c.rid
            WHERE p.rid=%s
            ORDER BY p.pid ASC
        """, (rid,))
        rows = cursor.fetchall()
        for row in rows:
            attach_image_url(row)
            if row.get("price") is not None:
                row["price"] = float(row["price"])
        return rows
    finally:
        cursor.close()
        db.close()


@app.post("/uploads")
async def upload_restaurant(
    restaurants: str = Form(None),
    rname: str = Form(None),
    file: UploadFile = File(...)
):
    restaurant_name = rname or restaurants or "Unnamed Restaurant"
    saved_filename, file_path = save_uploaded_file(file, "rest")

    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO restaurants (rname, images) VALUES (%s, %s)",
            (restaurant_name, saved_filename)
        )
        conn.commit()
        return {
            "success": True,
            "message": "Restaurant added successfully",
            "rid": cursor.lastrowid,
            "rname": restaurant_name,
            "images": f"{BASE_MEDIA_URL}{saved_filename}"
        }
    finally:
        cursor.close()
        conn.close()


@app.put("/api/restaurants/{rid}")
@app.post("/update_restaurant/{rid}")
async def update_restaurant(
    rid: int,
    rname: Optional[str] = Form(None),
    restaurants: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM restaurants WHERE rid=%s", (rid,))
        restaurant = cursor.fetchone()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        current_name = restaurant["rname"]
        current_image = restaurant["images"]

        new_name = rname or restaurants or name
        if new_name and new_name.strip():
            current_name = new_name.strip()

        if file and file.filename:
            saved_filename, file_path = save_uploaded_file(file, "rest")
            content = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)

            if current_image:
                old_path = os.path.join(IMAGES_DIR, os.path.basename(current_image))
                if os.path.exists(old_path):
                    os.remove(old_path)

            current_image = saved_filename

        cursor.execute(
            "UPDATE restaurants SET rname=%s, images=%s WHERE rid=%s",
            (current_name, current_image, rid)
        )
        conn.commit()

        return {
            "status": "success",
            "message": "Restaurant updated successfully",
            "rid": rid,
            "rname": current_name,
            "images": f"{BASE_MEDIA_URL}{current_image}"
        }
    finally:
        cursor.close()
        conn.close()


@app.delete("/delete_restaurant/{rid}")
@app.delete("/api/restaurants/{rid}")
async def delete_restaurant(rid: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT images FROM restaurants WHERE rid=%s", (rid,))
        row = cursor.fetchone()
        if row and row["images"]:
            path = os.path.join(IMAGES_DIR, os.path.basename(row["images"]))
            if os.path.exists(path):
                os.remove(path)

        cursor.execute("DELETE FROM restaurants WHERE rid=%s", (rid,))
        conn.commit()
        return {"status": "success", "deleted": rid}
    finally:
        cursor.close()
        conn.close()


# =========================================================
# PRODUCTS
# =========================================================

@app.post("/api/products")
async def add_product(
    rid: int = Form(...),
    catid: int = Form(...),
    product: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...)
):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT rid FROM restaurants WHERE rid=%s", (rid,))
        if not cursor.fetchone():
            raise HTTPException(status_code=400, detail="Restaurant not found")

        cursor.execute(
            "SELECT catid, rid, cat FROM category WHERE catid=%s AND rid=%s LIMIT 1",
            (catid, rid)
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Category does not belong to this restaurant"
            )

        saved_filename, file_path = save_uploaded_file(image, "product")
        content = await image.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        cursor.execute(
            "INSERT INTO products (rid, catid, product, images, price) VALUES (%s, %s, %s, %s, %s)",
            (rid, catid, product, saved_filename, price)
        )
        conn.commit()

        return {
            "status": "success",
            "message": "Product added successfully",
            "pid": cursor.lastrowid,
            "rid": rid,
            "catid": catid,
            "product": product,
            "price": price,
            "images": f"{BASE_MEDIA_URL}{saved_filename}"
        }
    finally:
        cursor.close()
        conn.close()


@app.get("/products")
@app.get("/api/products")
async def list_products(
    catid: Optional[int] = Query(None),
    rid: Optional[int] = Query(None)
):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT p.pid, p.rid, p.catid, p.product, p.product AS pname, p.images, p.price,
                   r.rname AS restaurant_name, c.cat AS category_name
            FROM products p
            INNER JOIN restaurants r ON p.rid = r.rid
            INNER JOIN category c ON p.catid = c.catid AND p.rid = c.rid
        """
        conditions = []
        params = []

        if rid is not None:
            conditions.append("p.rid=%s")
            params.append(rid)

        if catid is not None:
            conditions.append("p.catid=%s")
            params.append(catid)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Newest product should appear LAST in the list
        query += " ORDER BY p.pid ASC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        for row in rows:
            attach_image_url(row)
            if row.get("price") is not None:
                row["price"] = float(row["price"])

        return rows
    finally:
        cursor.close()
        conn.close()


@app.get("/category/{catid}/products")
@app.get("/api/category/{catid}/products")
@app.get("/api/categories/{catid}/products")
async def get_products_by_category(catid: int):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT catid, rid, cat FROM category WHERE catid=%s LIMIT 1", (catid,))
        category = cursor.fetchone()
        if category is None:
            raise HTTPException(status_code=404, detail=f"Category {catid} not found")

        category_rid = category["rid"]

        cursor.execute("""
            SELECT p.pid, p.rid, p.catid, p.product, p.images, p.price,
                   r.rname AS restaurant_name, c.cat AS category_name
            FROM products p
            INNER JOIN category c ON c.catid = p.catid AND c.rid = p.rid
            INNER JOIN restaurants r ON r.rid = p.rid
            WHERE p.catid=%s AND p.rid=%s
            ORDER BY p.pid ASC
        """, (catid, category_rid))

        products = cursor.fetchall()
        for product in products:
            attach_image_url(product)
            if product.get("price") is not None:
                product["price"] = float(product["price"])

        return {
            "success": True,
            "catid": catid,
            "rid": category_rid,
            "category": category["cat"],
            "count": len(products),
            "products": products
        }
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.get("/restaurants/{rid}/category/{catid}/products")
@app.get("/api/restaurants/{rid}/category/{catid}/products")
def get_restaurant_category_products(rid: int, catid: int):
    conn = None
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT catid, rid, cat FROM category WHERE catid=%s AND rid=%s LIMIT 1",
            (catid, rid)
        )
        category = cursor.fetchone()
        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f"Category {catid} does not belong to restaurant {rid}"
            )

        cursor.execute("""
            SELECT p.pid, p.rid, p.catid, p.product, p.product AS pname, p.images, p.price,
                   r.rname AS restaurant_name, c.cat AS category_name
            FROM products p
            INNER JOIN restaurants r ON r.rid = p.rid
            INNER JOIN category c ON c.catid = p.catid AND c.rid = p.rid
            WHERE p.rid=%s AND p.catid=%s
            ORDER BY p.pid ASC
        """, (rid, catid))

        rows = cursor.fetchall()
        for row in rows:
            attach_image_url(row)
            if row.get("price") is not None:
                row["price"] = float(row["price"])

        return {
            "success": True,
            "rid": rid,
            "catid": catid,
            "category": category["cat"],
            "count": len(rows),
            "products": rows
        }
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.delete("/delete_product/{pid}")
@app.delete("/api/products/{pid}")
async def delete_product(pid: int):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT images FROM products WHERE pid=%s", (pid,))
        row = cursor.fetchone()
        if row and row["images"]:
            path = os.path.join(IMAGES_DIR, os.path.basename(row["images"]))
            if os.path.exists(path):
                os.remove(path)

        cursor.execute("DELETE FROM products WHERE pid=%s", (pid,))
        conn.commit()
        return {"status": "success", "deleted": pid}
    finally:
        cursor.close()
        conn.close()


# =========================================================
# CART
# =========================================================

@app.post("/add-cart")
def add_cart(data: Cart):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT pid FROM products WHERE pid=%s", (data.pid,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute("INSERT INTO cart (uid, pid) VALUES (%s, %s)", (data.uid, data.pid))
        db.commit()
        return {"success": True, "message": "Added to cart"}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Product already in cart")
    finally:
        cursor.close()
        db.close()


@app.get("/cart/{uid}", response_model=List[CartItemResponse])
def get_user_cart(uid: int):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.pid, p.rid, p.product, p.price, p.images
            FROM cart c
            INNER JOIN products p ON c.pid = p.pid
            WHERE c.uid=%s
        """, (uid,))
        results = cursor.fetchall()

        for row in results:
            if row.get("images"):
                row["image"] = f"{BASE_MEDIA_URL}{row['images']}"
                del row["images"]
            else:
                row["image"] = ""

            if row.get("price") is not None:
                row["price"] = float(row["price"])

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
        cursor.execute("DELETE FROM cart WHERE uid=%s AND pid=%s", (uid, pid))
        db.commit()
        if cursor.rowcount == 0:
            return {"success": False, "message": "Item not found"}
        return {"success": True, "message": "Item removed from cart"}
    finally:
        cursor.close()
        db.close()


# =========================================================
# ORDERS
# =========================================================

@app.post("/place-order")
def place_order(order_data: PlaceOrder):
    db = get_db()
    cursor = db.cursor()
    try:
        if not order_data.items:
            raise HTTPException(status_code=400, detail="No items found in order payload")

        if not order_data.address or not order_data.address.strip():
            raise HTTPException(status_code=400, detail="Delivery address cannot be empty")

        insert_query = """
            INSERT INTO orders (pid, uid, price, quantity, address, paymenttype, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        """

        for item in order_data.items:
            qty = item.quantity if item.quantity and item.quantity > 0 else 1
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

        cursor.execute("DELETE FROM cart WHERE uid=%s", (order_data.uid,))
        db.commit()
        return {"success": True, "message": "Your purchase records have been submitted!"}
    except Error:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database transaction processing failure")
    finally:
        cursor.close()
        db.close()


@app.get("/orders/{uid}", response_model=List[OrderItemResponse])
def get_user_orders(uid: int):
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT o.oid, o.pid, o.uid,
                   COALESCE(u.username, 'Unknown User') AS username,
                   u.phone AS phone,
                   COALESCE(p.product, 'Unknown Product') AS product,
                   o.price, o.quantity, o.address, o.paymenttype, o.status, p.images
            FROM orders o
            LEFT JOIN products p ON o.pid = p.pid
            LEFT JOIN `user` u ON o.uid = u.uid
            WHERE o.uid=%s
            ORDER BY o.oid DESC
        """, (uid,))
        results = cursor.fetchall()

        for row in results:
            if row.get("images"):
                row["image"] = f"{BASE_MEDIA_URL}{row['images']}"
                del row["images"]
            else:
                row["image"] = ""

            if row.get("price") is not None:
                row["price"] = float(row["price"])

        return results
    finally:
        cursor.close()
        connection.close()


@app.get("/orders")
@app.get("/api/orders")
async def list_orders():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT o.oid, o.pid, o.uid,
                   COALESCE(u.username, 'Unknown User') AS username,
                   u.phone AS phone,
                   COALESCE(p.product, 'Unknown Product') AS product,
                   o.price, o.quantity, o.address, o.paymenttype, o.status, p.images
            FROM orders o
            LEFT JOIN products p ON o.pid = p.pid
            LEFT JOIN `user` u ON o.uid = u.uid
            ORDER BY o.oid DESC
        """)
        rows = cursor.fetchall()

        for row in rows:
            if row.get("images"):
                row["image"] = f"{BASE_MEDIA_URL}{row['images']}"
                del row["images"]
            else:
                row["image"] = ""

            if row.get("price") is not None:
                row["price"] = float(row["price"])

        return rows
    finally:
        cursor.close()
        conn.close()


@app.put("/api/orders/{oid}/status")
async def update_order_status(oid: int, status_update: OrderStatusUpdate):
    valid_statuses = ["pending", "on the way", "delivered"]
    new_status = status_update.status.strip().lower()

    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status assignment. Must be one of: " + ", ".join(valid_statuses)
        )

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status=%s WHERE oid=%s", (new_status, oid))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order ID not found")

        return {"status": "success", "updated_oid": oid, "new_status": new_status}
    finally:
        cursor.close()
        conn.close()


@app.delete("/orders/remove/{uid}/{pid}")
def remove_order_item(uid: int, pid: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE uid=%s AND pid=%s", (uid, pid))
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
        cursor.execute("DELETE FROM orders WHERE oid=%s", (oid,))
        conn.commit()
        return {"status": "success", "deleted": oid}
    finally:
        cursor.close()
        conn.close()


# =========================================================
# USERS
# =========================================================

@app.get("/users")
@app.get("/api/users")
async def list_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT uid, username, phone, phone AS mobile
            FROM `user`
            ORDER BY uid DESC
        """)
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
        cursor.execute("DELETE FROM cart WHERE uid=%s", (uid,))
        cursor.execute("DELETE FROM orders WHERE uid=%s", (uid,))
        cursor.execute("DELETE FROM `user` WHERE uid=%s", (uid,))
        conn.commit()
        return {"status": "success", "deleted": uid}
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()