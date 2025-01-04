import pika
import json
import time

class MessageBus:
    def __init__(self, host="rabbitmq"):
        self.host = host

    def publish(self, queue, message: dict):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            channel = connection.channel()
            channel.queue_declare(queue=queue)
            channel.basic_publish(exchange="", routing_key=queue, body=json.dumps(message))
            print(f"Message sent to {queue}: {message}")
            channel.close()
            connection.close()
        except Exception as e:
            print(f"Failed to send message: {e}")
            raise

    def start_listening(self, queue, callback):
        retries = 5
        while retries > 0:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
                channel = connection.channel()
                channel.queue_declare(queue=queue)
                channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
                print(f"Listening to {queue}...")
                channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                print(f"RabbitMQ not ready. Retrying in 5 seconds... ({retries} retries left)")
                retries -= 1
                time.sleep(5)
            except Exception as e:
                print(f"Error in start_listening: {e}")
                break
