import redis
import json

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.r = redis.Redis(host='localhost', port=6388, db=0)
        self.pubsub = self.r.pubsub()
        self.pubsub.subscribe("chat")

    def send_message(self, message):
        self.r.publish("chat", json.dumps({"user": self.username, "text": message}))

    def receive_messages(self, callback):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data['user'] != self.username:
                    callback(data)