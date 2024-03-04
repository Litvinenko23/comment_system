import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from comments_app.models import Comment


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "comments"
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("text_data", text_data)

        # Получение данных из вебсокета
        text_data_json = json.loads(text_data)
        print(text_data_json)

        # Postman:
        # message = text_data_json[0]['message']
        # parent_comment_id = text_data_json[1]['parent_comment_id']  # Получаем ID родительского комментария, если есть

        # Browser:
        message = text_data_json['message']
        parent_comment_id = text_data_json.get('parent_comment_id')  # Получаем ID родительского комментария, если есть

        print("parent_comment_id", parent_comment_id)

        comment = await self.save_comment_to_database(message, parent_comment_id)

        # Отправка сообщения всем подключенным клиентам
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def save_comment_to_database(self, message, parent_comment_id):

        if parent_comment_id:
            parent_comment = await database_sync_to_async(Comment.objects.get)(id=parent_comment_id)
            new_comment = await database_sync_to_async(Comment.objects.create)(message=message,
                                                                               parent_comment=parent_comment)
        else:
            new_comment = await database_sync_to_async(Comment.objects.create)(message=message)
        return new_comment


    async def chat_message(self, event):
        # Получаем сообщение из события
        message = event["message"]

        # print("hello from consumer chat_message")
        print(message + "AAA")

        # Отправляем сообщение всем клиентам, подключенным к веб-сокету
        await self.send(text_data=json.dumps({"message": message}))


