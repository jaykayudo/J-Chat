from sqlite3 import Timestamp
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()




class ChatRoom(models.Model):
    name = models.CharField(max_length=120,unique=True)
    description = models.CharField(max_length=1000,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Messages(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    chat_room = models.CharField(max_length=120,default="chat_general")
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.author.username

    def last_10_messages(room_name):
        return list(reversed(Messages.objects.filter(chat_room = room_name).order_by('-timestamp')[:30]))