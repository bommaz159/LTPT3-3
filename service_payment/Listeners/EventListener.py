from Infrastructure.PaymentRepository import PaymentRepository
import json

class EventListener:
    def __init__(self):
        self.payment_repository = PaymentRepository()

    def handle_order_created(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            order_id = message["order_id"]
            amount = message["amount"]

            # Ghi vào database của service_payment
            success, msg = self.payment_repository.save_order(order_id, amount)
            if success:
                print(f"Order {order_id} saved with amount {amount} in payment service.")
            else:
                print(f"Failed to save order {order_id}: {msg}")
        except Exception as e:
            print(f"Error processing order_created event: {e}")

