import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LivestreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'livestream_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_type = text_data_json.get('type')

        if message_type == 'comment':
            # Handle comment logic, e.g., save to database
            # Modify as per your Comment model structure
            user = self.scope["user"]
            comment_text = message
            # Save the comment to the database
            # Comment.objects.create(user=user, video=video_instance, text=comment_text)
        elif message_type == 'gift':
            # Handle gift logic, e.g., save to database
            # Modify as per your Gift model structure
            user = self.scope["user"]
            gift_path = message
            # Save the gift to the database
            # Gift.objects.create(user=user, video=video_instance, path=gift_path)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'type': message_type,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
