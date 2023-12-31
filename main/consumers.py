import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class LiveStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'live_stream_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'live_stream_group',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        is_like = data.get('like', False)
        ar_gift_image = data.get('ar_gift_image', None)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message, 'like': is_like, 'ar_gift_image': ar_gift_image}))

        # Handle the received message (if needed)
        print('Received message:', message)

        # Additional handling for likes, AR gifts, etc.
        if is_like:
            await self.send(text_data=json.dumps({'message': f'{message} - Like received!', 'like': True}))
        elif ar_gift_image:
            await self.send(text_data=json.dumps({'message': f'{message} - AR gift received!', 'ar_gift_image': ar_gift_image}))

    async def send_live_stream_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))