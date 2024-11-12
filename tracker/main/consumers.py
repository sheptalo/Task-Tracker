import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from main.models import UserModel


class Notifications(WebsocketConsumer):
    def connect(self):
        uid = self.scope.get("query_string").decode("utf-8").split("id=")[1]
        user = UserModel.objects.get(id=uid)
        print(user.group_name)
        self.room_group_name = user.group_name

        async_to_sync(self.channel_layer.group_add)(
            user.group_name, self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print("a")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({"message": message}))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def notify_user(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
