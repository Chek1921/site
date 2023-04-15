import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("online", self.channel_name)
        print(self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def user_commented(self, text_data):
        print(text_data)
        await self.send(json.dumps({
            "type": "report.answer",
            "text": text_data["message"],
            "username": text_data["username"],
        }))


