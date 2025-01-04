from Entities.Order import Order
from Infrastructure.OrderRepository import OrderRepository
from Infrastructure.MessageBus import MessageBus

class CreateOrder:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.message_bus = MessageBus()

    def execute(self, order_id, customer_name, amount):
        order = Order(order_id, customer_name, amount)
        success, message = self.order_repository.save_order(order)
        if not success:
            return False, message

        # Gửi sự kiện `order_created`
        event_message = {
            "event": "order_created",
            "order_id": order_id,
            "customer_name": customer_name,
            "amount": amount,
        }
        self.message_bus.publish("order_events", event_message)  # Gửi sự kiện đến RabbitMQ
        return True, "Order created successfully"
