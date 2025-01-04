from flask import request, jsonify
from UseCases.CreateOrder import CreateOrder

class OrderController:
    def __init__(self):
        self.create_order_use_case = CreateOrder()

    def create_order(self):
        data = request.json
        order_id = data.get("order_id")
        customer_name = data.get("customer_name")
        amount = data.get("amount")

        if not order_id or not customer_name or amount is None:
            return jsonify({"error": "Missing required fields"}), 400
        if amount < 0:
            return jsonify({"error": "Số tiền phải là giá trị không âm"}), 400

        success, message = self.create_order_use_case.execute(order_id, customer_name, amount)
        if success:
            return jsonify({"message": message}), 201
        else:
            return jsonify({"error": message}), 500
