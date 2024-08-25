import redis
import time

class ChatBackend:
    def __init__(self, channel):
        # Connect to Redis
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.channel = channel
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)

    def publish_message(self, message):
        """Publish a message to the channel."""
        self.redis_client.publish(self.channel, message)
        timestamp = int(time.time())
        self.redis_client.rpush(f"history:{self.channel}", f"{timestamp}:{message}")

    def get_message_history(self):
        """Retrieve the message history for the channel."""
        history = self.redis_client.lrange(f"history:{self.channel}", 0, -1)
        return [msg.decode('utf-8') for msg in history]

    def listen_messages(self):
        """Listen for new messages on the channel."""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                yield message['data'].decode('utf-8')
