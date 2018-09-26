from django.db import models

# Create your models here.
from django.utils import timezone

from blog.models import upload_location


class Icon(models.Model):
    icon_name = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.icon_name


class MediaFiles(models.Model):
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    video = models.FileField(upload_to=upload_location, blank=True, null=True)
    file = models.FileField(upload_to=upload_location, blank=True,  null=True)
    order = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)



