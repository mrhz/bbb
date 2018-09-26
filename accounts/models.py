from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
from buildino import settings


class Profile(models.Model):
    GENDER_CHOICE = (('male', 'Male'),
                     ('female', 'Female'))
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, blank=True, null=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    address = GenericRelation('Address', blank=True, null=True)
    phone = GenericRelation('Phone_number', blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to='photo/Profile', null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def get_profile_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return "/static/assets/base/img/content/team/user1.jpg"

class Country(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    address = models.CharField(max_length=255, )
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, )
    title = models.CharField(max_length=120, )
    description = models.CharField(max_length=120, null=True, blank=True)
    lat = models.CharField(max_length=30, null=True, blank=True)
    lng = models.CharField(max_length=30, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title + self.address


class Phone_Number(models.Model):
    number = models.IntegerField()
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    # Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.number)
