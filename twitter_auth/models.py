from django.db import models
from django.utils import timezone
from .validators import validate_file_extension
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    text = models.TextField(max_length=2200, blank=False, null=False)
    # photo_address =
    # thumbnail=models.ImageField(blank=True, null=True)
    # creator=models
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    media = models.ImageField(blank=True, null=True, upload_to='images/', validators=[validate_file_extension])
    # media=models.FileField

    def __str__(self):
        return self.text

    def publish(self):
        self.published_date = timezone.now()
        self.save()

# class MyUser(User):
#     telegram_channel_id = models.CharField(blank=True, null=True)
#
#     def __str__(self):
#         return self.username

# class TelegramInfo(models.Model):
#     channel_id = models.CharField(blank=False, null=False)
#
#     def __str__(self):
#         return self.channel_id