import redis
import time
import hashlib


class ChatBackend:
    def __init__(self):
        # Connect to Redis
        self.redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
        self.pubsub = None
        self.channel = None

    def hash_password(self, password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """Register a new user."""
        if self.redis_client.hexists("users", username):
            return False  # Username already exists
        hashed_password = self.hash_password(password)
        self.redis_client.hset("users", username, hashed_password)
        return True

    def authenticate_user(self, username, password):
        """Authenticate a user."""
        hashed_password = self.hash_password(password)
        stored_password = self.redis_client.hget("users", username)
        if stored_password and stored_password.decode("utf-8") == hashed_password:
            return True
        return False

    def set_channel(self, channel):
        """Set the chat channel."""
        self.channel = channel
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)

    def publish_message(self, message):
        """Publish a message to the channel."""
        if not self.channel:
            raise Exception("Channel not set. Please join a channel first.")
        self.redis_client.publish(self.channel, message)
        timestamp = int(time.time())
        self.redis_client.rpush(f"history:{self.channel}", f"{timestamp}:{message}")

    def get_message_history(self):
        """Retrieve the message history for the channel."""
        if not self.channel:
            raise Exception("Channel not set. Please join a channel first.")
        history = self.redis_client.lrange(f"history:{self.channel}", 0, -1)
        return [msg.decode("utf-8") for msg in history]

    def listen_messages(self):
        """Listen for new messages on the channel."""
        if not self.channel:
            raise Exception("Channel not set. Please join a channel first.")
        for message in self.pubsub.listen():
            if message["type"] == "message":
                yield message["data"].decode("utf-8")
