import threading
from flask import Flask
from Controllers.PaymentController import PaymentController
from Infrastructure.MessageBus import MessageBus
from Listeners.EventListener import EventListener

app = Flask(__name__)
payment_controller = PaymentController()
message_bus = MessageBus()
event_listener = EventListener()

@app.route("/payment", methods=["POST"])
def process_payment():
    return payment_controller.process_payment()

if __name__ == "__main__":
    #nghe `order_created` từ RabbitMQ
    listener_thread = threading.Thread(
        target=message_bus.start_listening,
        args=("order_events", event_listener.handle_order_created),
        daemon=True
    )
    listener_thread.start()

    app.run(host="0.0.0.0", port=5001)

