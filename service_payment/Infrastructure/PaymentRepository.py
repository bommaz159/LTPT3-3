from Infrastructure.Database import Database
from Entities.Payment import Payment

class PaymentRepository:
    def __init__(self):
        Database.init_db()

    def save_payment(self, payment):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM payments WHERE payment_id = ?', (payment.payment_id,))
            existing_payment = cursor.fetchone()
            if existing_payment:
                return False, f"Payment ID {payment.payment_id} already exists."
            cursor.execute('INSERT INTO payments (payment_id, order_id, amount) VALUES (?, ?, ?)',(payment.payment_id, payment.order_id, payment.amount))
            conn.commit()
            conn.close()
            return True, "Payment saved successfully"
        except Exception as e:
            return False, str(e)
    
    def save_order(self, order_id, amount):
        """Ghi thông tin đơn hàng vào orders.db."""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS orders (order_id TEXT PRIMARY KEY,amount REAL)''')

            cursor.execute('INSERT INTO orders (order_id, amount) VALUES (?, ?)', (order_id, amount))
            conn.commit()
            conn.close()
            return True, "Order saved successfully"
        except Exception as e:
            print(f"Failed to save order: {e}")
            return False, str(e)
            
    def get_order(self, order_id):
        """Lấy thông tin đơn hàng từ cơ sở dữ liệu cục bộ."""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT order_id, amount FROM orders WHERE order_id = ?', (order_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return {"order_id": row[0], "amount": row[1]}
            return None
        except Exception as e:
            print(f"Failed to get order: {e}")
            return None