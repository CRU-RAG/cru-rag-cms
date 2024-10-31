"""Message producer service"""
import os
from concurrent.futures import ThreadPoolExecutor
import pika

class Producer:
    """Service to produce messages to RabbitMQ."""
    def __init__(self):
        """Initialize the producer service."""
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.credentials = pika.PlainCredentials(
            os.environ.get("RABBIT_MQ_USERNAME"),
            os.environ.get("RABBIT_MQ_PASSWORD")
        )
        self.connection_params = pika.ConnectionParameters(
            os.environ.get("RABBIT_MQ_HOST"),
            os.environ.get("RABBIT_MQ_PORT"),
            os.environ.get("RABBIT_MQ_VHOST"),
            self.credentials,
        )

    def publish_message(self, message):
        """Publish a message to RabbitMQ."""
        self.executor.submit(self._send_message, message)

    def _send_message(self, message):
        """Send a message to RabbitMQ."""
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.queue_declare(
            queue=os.environ.get("RABBIT_MQ_QUEUE")
        )
        channel.basic_publish(
            exchange='', routing_key=os.environ.get("RABBIT_MQ_QUEUE"), body=message
        )
        connection.close()
