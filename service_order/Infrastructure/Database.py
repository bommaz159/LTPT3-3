import sqlite3
import os

class Database:
    DB_PATH = os.path.join("data", "orders.db")

    @staticmethod
    def init_db():
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(Database.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (order_id TEXT PRIMARY KEY,customer_name TEXT,amount REAL,status TEXT DEFAULT 'chưa thanh toán')''')
        conn.commit()
        conn.close()

    @staticmethod
    def get_connection():
        return sqlite3.connect(Database.DB_PATH)
