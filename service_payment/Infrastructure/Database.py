import sqlite3
import os

class Database:
    DB_PATH = os.path.join("data", "payments.db") 

    @staticmethod
    def init_db():
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(Database.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS payments (payment_id TEXT PRIMARY KEY,order_id TEXT,amount REAL)''')
        conn.commit()
        conn.close()

    @staticmethod
    def get_connection():
        return sqlite3.connect(Database.DB_PATH)
