import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']

        # 验证用户是否是会话的参与者
        if self.user.is_anonymous or not await self.is_participant():
            await self.close()
            return

        # 加入房间组
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开房间组
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    # 从 WebSocket 接收消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        # 创建新消息
        new_message = await self.create_message(message_text)

        # 将消息发送到房间组
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': new_message.id,
                    'sender': new_message.sender.username,
                    'text': new_message.text,
                    'created_at': new_message.created_at.isoformat(),
                    'is_me': False # 对于接收者来说，这条消息不是他们自己发的
                }
            }
        )

    # 从房间组接收消息
    async def chat_message(self, event):
        message_data = event['message']

        # 调整 is_me 字段
        # 如果消息的发送者是当前consumer的用户，则is_me为True
        if message_data['sender'] == self.user.username:
            message_data['is_me'] = True

        # 将消息发送到 WebSocket
        await self.send(text_data=json.dumps(message_data))

    @database_sync_to_async
    def is_participant(self):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return self.user in conversation.participants.all()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def create_message(self, message_text):
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=self.user,
            text=message_text
        )
        # 更新会话的 updated_at 时间戳
        conversation.save()
        return message
