from email import message
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from chat.models import Messages, User
from django.contrib.auth.models import AnonymousUser

class ChatConsumer(WebsocketConsumer):
   
        
    def fetch_messages(self,data):
        messages = Messages.last_10_messages(self.room_group_name)
        content = self.messages_json(messages)
        
        self.send_message(content)

    def messages_json(self,data):
        result = []
        for message in data:
            result.append(self.message_json(message))
        return result
    def message_json(self,data):
        return {
            'author': data.author.username,
            'message':data.content,
            'timestamp':str(data.timestamp)
        }
    def new_message(self,data):
        if data['from']:
            author = User.objects.filter(username = data['from'])[0]
        else:
            author = AnonymousUser()
        message = Messages.objects.create(author = author,content = data['message'], chat_room = self.room_group_name)
        data = {
            'author': message.author.username,
            'message':message.content,
            'timestamp':str(message.timestamp)
        }
        self.send_chat_message(data)

    command = {
        'fetch_message':fetch_messages,
        'new_message':new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.headers = {}
        for x,y in self.scope['headers']:
            self.headers[x.decode()] = y.decode()
        # print(self.headers['user-agent'])
        # print(self.channel_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        del self.headers

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        # message = data['message']
        self.command[data['command']](self,data)
        # self.new_message(data)
        # Send message to room group

    def send_chat_message(self,message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    def send_message(self,message):
        self.send(text_data = json.dumps(message))
    # Receive message from room group
    def chat_message(self, event):
        message = event['message'] 

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
    

class PersonalChatConsumer(WebsocketConsumer):
    def get_chat_name(self):
        self.sender = self.scope['url_route']['kwargs']['sender']
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        chat_name1 = f'chat_{self.sender}_{self.receiver}'
        chat_name2 = f'chat_{self.receiver}_{self.sender}'
        chat_room =  Messages.objects.all().values_list('chat_room')
        if chat_room:
            map_chat_room = list(map(lambda x: x[0], list(chat_room)))
            if chat_name1 in map_chat_room:
                return chat_name1
            elif chat_name2 in map_chat_room:
                return chat_name2
        return chat_name1
        

    def connect(self):
        self.sender = self.scope['url_route']['kwargs']['sender']
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        if self.sender != self.scope['user'].username:
            self.close(code = 1423)
            return
        if not User.objects.filter(username = self.receiver).exists() or self.sender == self.receiver:
            self.close(code = 1423)
            return
        
        self.chat_name = self.get_chat_name()
        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name
        )
        self.accept()
    def diconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name,
            self.channel_name
        )

    def fetch_messages(self,data):
        message = Messages.last_10_messages(self.chat_name)
        result = self.messages_json(message)
        self.send_message(result)

    def new_message(self,data):
        if data['from']:
            author = User.objects.filter(username = data['from'])[0]
        else:
            return
        if not author:
            return
        message = Messages.objects.create(author = author,content = data['message'], chat_room = self.chat_name)
        data = {
            'author': message.author.username,
            'message':message.content,
            'timestamp':str(message.timestamp)
        }
        self.send_message(data)
    def messages_json(self,data):
        result = []
        for message in data:
            result.append(self.message_json(message))
        return result
    def message_json(self,data):
        return {
            'author': data.author.username,
            'message':data.content,
            'timestamp':str(data.timestamp)
        }

    command = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }

    def receive(self, text_data):
        message = json.loads(text_data)
        if message['command'] in self.command:
            self.command[message['command']](self,message)

    def send_message(self,data):
        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            {
                'type':'chat_message',
                'message':data
            }
        )
    def chat_message(self,event):
        message = event['message']
        self.send(text_data = json.dumps(message))


        
