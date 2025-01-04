from flask import Flask, request, jsonify
import threading
from UseCases.CreateOrder import CreateOrder
from Infrastructure.MessageBus import MessageBus
from Infrastructure.OrderRepository import OrderRepository
import json

app = Flask(__name__)
create_order_use_case = CreateOrder()
message_bus = MessageBus()
order_repository = OrderRepository()

@app.route("/order", methods=["POST"])
def create_order():
    data = request.json
    order_id = data.get("order_id")
    customer_name = data.get("customer_name")
    amount = data.get("amount")

    if not order_id or not customer_name or amount is None:
        return jsonify({"error": "Missing required fields"}), 400

    if amount < 0:
        return jsonify({"error": "Amount must be a non-negative value"}), 400

    success, message = create_order_use_case.execute(order_id, customer_name, amount)
    if not success:
        return jsonify({"error": message}), 500

    return jsonify({"message": "Order created successfully"}), 201

@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    order = order_repository.get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

def payment_callback(ch, method, properties, body):
    """Callback xử lý sự kiện thanh toán từ RabbitMQ."""
    try:
        message = json.loads(body)
        order_id = message.get("order_id")
        status = "đã thanh toán"

        if order_id:
            success, msg = order_repository.update_order_status(order_id, status)
            if success:
                print(f"Order {order_id} status updated to {status}")
            else:
                print(f"Failed to update order {order_id}: {msg}")
    except Exception as e:
        print(f"Error processing payment message: {e}")

if __name__ == "__main__":
    listener_thread = threading.Thread(
        target=message_bus.start_listening,
        args=("payment_queue", payment_callback),
        daemon=True
    )
    listener_thread.start()

    app.run(host="0.0.0.0", port=5000)
