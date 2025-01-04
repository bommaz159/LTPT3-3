from Infrastructure.Database import Database
from Entities.Order import Order

class OrderRepository:
    def __init__(self):
        Database.init_db()

    def save_order(self, order):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO orders (order_id, customer_name, amount, status) VALUES (?, ?, ?, ?)',(order.order_id, order.customer_name, order.amount, "chưa thanh toán"))
            conn.commit()
            conn.close()
            return True, "Order saved successfully"
        except Exception as e:
            return False, str(e)

    def update_order_status(self, order_id, status):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE orders SET status = ? WHERE order_id = ?', (status, order_id))
            conn.commit()
            conn.close()
            return True, "Order status updated successfully"
        except Exception as e:
            return False, str(e)

    def get_order(self, order_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT order_id, customer_name, amount, status FROM orders WHERE order_id = ?', (order_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "order_id": row[0],
                "customer_name": row[1],
                "amount": row[2],
                "status": row[3]
            }
        else:
            return None

    def get_order_amount(self, order_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT amount FROM orders WHERE order_id = ?', (order_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
