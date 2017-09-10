from django.db import models
from django.utils import timezone
from .validators import validate_file_extension

# Create your models here.
class Post(models.Model):
    text = models.TextField(max_length=140, blank=False, null=False)
    # photo_address =
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    media = models.ImageField(blank=True, null=True, upload_to='images/', validators=[validate_file_extension])

    def __str__(self):
        return self.text

    def publish(self):
        self.published_date = timezone.now()
        self.save()