import pika

from broker.events import PublicationResourceEvent


class MessageProducer:
    def __init__(self, host: str, queue: str):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def _ensure_connection(self):
        if self.connection is None or self.connection.is_closed:
            self._connect()
        if self.channel is None or self.channel.is_closed:
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)

    def send_message(self, message):
        try:
            self._ensure_connection()
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=message.model_dump_json().encode('utf-8')
            )
        except:
            self._reconnect()
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=message.model_dump_json().encode('utf-8')
            )

    def _reconnect(self):
        self.connection.close()
        self._connect()

    def close_connection(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


message_producer = MessageProducer('50.19.40.173', 'recursos')
