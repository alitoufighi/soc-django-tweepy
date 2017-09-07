from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    text = models.TextField(max_length=140, blank=False, null=False)
    # photo_address =
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.text

    def publish(self):
        self.published_date = timezone.now()
        self.save()