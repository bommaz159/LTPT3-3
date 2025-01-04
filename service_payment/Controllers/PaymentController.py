from flask import request, jsonify
from UseCases.ProcessPayment import ProcessPayment

class PaymentController:
    def __init__(self):
        self.process_payment_use_case = ProcessPayment()

    def process_payment(self):
        data = request.json
        order_id = data.get("order_id")
        amount = data.get("amount")
        if not order_id or not amount:
            return jsonify({"error": "Thiếu thông tin bắt buộc"}), 400

        success, result = self.process_payment_use_case.execute(order_id, amount)
        if success:
            return jsonify({"message": "Thanh toán thành công", "payment_id": result}), 201
        else:
            return jsonify({"error": result}), 400