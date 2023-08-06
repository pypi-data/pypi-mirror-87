"""
Module providing helpers to deal with RabbitMQ
"""

from typing import Callable

import pika
from pika_utils.blocking import RecoverableBlockingPublisher, RecoverableBlockingConsumer
from pika_utils import build_connection_parameters


class RecoverableBlockingConsumerPublisher:
    def __init__(
            self,
            params: pika.connection.Parameters,
            configure_consumer_channel: Callable,
            configure_publisher_channel: Callable,
            max_reconnection_retries: int = 0,
            backoff_factor: float = 0.0,
    ):
        self.consumer = RecoverableBlockingConsumer(
            params,
            configure_consumer_channel,
            max_reconnection_retries,
            backoff_factor
        )
        self.publisher = RecoverableBlockingPublisher(
            params,
            configure_publisher_channel,
            max_reconnection_retries,
            backoff_factor
        )

    def basic_publish(self, *args, **kwargs):
        self.publisher.basic_publish(*args, **kwargs)

    def start_consuming(self):
        self.consumer.start()

    def stop_consuming(self):
        self.consumer.stop()
