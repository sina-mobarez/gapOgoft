import redis
from PyQt6.QtCore import QObject, pyqtSignal, QThread


class RedisListenerThread(QThread):
    message_received = pyqtSignal(str, str)

    def __init__(self, redis_client):
        super().__init__()
        self.redis_client = redis_client
        self.pubsub = self.redis_client.pubsub()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            message = self.pubsub.get_message(timeout=1.0)
            if message and message["type"] == "message":
                channel = message["channel"].decode()
                data = message["data"].decode()
                self.message_received.emit(channel, data)

    def stop(self):
        self.running = False
        self.pubsub.close()


class RedisManager(QObject):
    message_received = pyqtSignal(str, str)

    def __init__(self, host="localhost", port=6379, db=0):
        super().__init__()
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        self.listener_thread = RedisListenerThread(self.redis_client)
        self.listener_thread.message_received.connect(self.on_message_received)
        self.listener_thread.start()

    def publish(self, channel, message):
        self.redis_client.publish(channel, message)

    def subscribe(self, channel):
        self.listener_thread.pubsub.subscribe(channel)

    def unsubscribe(self, channel):
        self.listener_thread.pubsub.unsubscribe(channel)

    def on_message_received(self, channel, message):
        self.message_received.emit(channel, message)

    def cleanup(self):
        self.listener_thread.stop()
        self.listener_thread.wait()
