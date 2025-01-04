from Infrastructure.PaymentRepository import PaymentRepository
from Infrastructure.MessageBus import MessageBus
from Entities.Payment import Payment
import uuid

class ProcessPayment:
    def __init__(self):
        self.payment_repository = PaymentRepository()
        self.message_bus = MessageBus()

    def execute(self, order_id, amount):
        """
        Xử lý thanh toán cho một đơn hàng.
        """
        try:
            # Lấy thông tin đơn hàng từ orders.db
            order = self.payment_repository.get_order(order_id)
            if not order:
                return False, f"Order ID {order_id} not found in payment service"
            order_amount = order["amount"]
            if amount != order_amount:
                return False, f"Payment amount {amount} does not match order amount {order_amount}."
            payment_id = str(uuid.uuid4())

            # Lưu thanh toán vào payments.db
            payment = Payment(payment_id, order_id, amount)
            success, message = self.payment_repository.save_payment(payment)
            if not success:
                return False, message

            # Gửi thông báo qua RabbitMQ
            notification_message = {
                "order_id": order_id,
                "payment_id": payment_id,
                "amount": amount,
                "message": f"Payment {payment_id} for order {order_id} was processed successfully."
            }
            self.message_bus.publish("payment_queue", notification_message)
            return True, payment_id

        except Exception as e:
            print(f"Error processing payment: {e}")
            return False, f"An error occurred: {str(e)}"
