import pika

QUEUE_NAME = "mailbox"


def callback(channel, method, properties, body):
    message = body.decode("utf-8")
