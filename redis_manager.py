import redis


class RedisManager:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.pubsub = self.redis.pubsub()

    def publish(self, channel, message):
        self.redis.publish(channel, message)

    def subscribe(self, channel, callback):
        self.pubsub.subscribe(**{channel: callback})

    def run_in_thread(self, sleep_time=0.001):
        self.pubsub.run_in_thread(sleep_time=sleep_time)
