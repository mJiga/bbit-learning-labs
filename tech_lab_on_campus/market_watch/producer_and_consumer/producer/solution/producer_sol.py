import os
import sys
import pika
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from producer_interface import mqProducerInterface


class mqProducer(mqProducerInterface) :
    def __init__(self, routing_key, exchange_name) -> None:
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        #Build our connection to the RMQ Connection.
        #The AMPQ_URL is a string which tells pika the package the URL of our AMPQ service in this scenario RabbitMQ.
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        
        # Establish Channel
        self.channel = self.connection.channel()

        # Create the exchange if not already present
        exchange = self.channel.exchange_declare(exchange=self.exchange_name)

    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )

        # Close Channel
        self.channel.close()

        # Close Connection
        self.connection.close()
