from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
# Create your models here.
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from accounts.models import Address
from blog.models import upload_location


class Standard(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=500, blank=True)
    trashed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Agency(models.Model):
    STATUS_CHOICE = (('pending', 'Pending'),
                     ('accepted', 'Accepted'),
                     ('rejected', 'Rejected'),

                     )
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=upload_location, null=True, blank=True)
    logo_thumbnail = ImageSpecField(source='logo',
                                    processors=[ResizeToFill(750, 750)],
                                    format='JPEG',
                                    options={'quality': 90})
    # address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, verbose_name=_('آدرس'))
    address = GenericRelation(Address)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='agencies', )
    commercial_code = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Brand(models.Model):
    STATUS_CHOICE = (('pending', 'Pending'),
                     ('accepted', 'Accepted'),
                     ('rejected', 'Rejected'),
                     )

    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=upload_location, null=True, blank=True)
    logo_thumbnail = ImageSpecField(source='logo',
                                    processors=[ResizeToFill(500, 500)],
                                    format='JPEG',
                                    options={'quality': 90})
    owner = models.ForeignKey(Agency, on_delete=models.PROTECT, related_name='owning_brands', )
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending', )
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    # TODO: One of these fields is required
    country = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    id_code = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=20, blank=True)
    standards = models.ManyToManyField('Standard', blank=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reseller(models.Model):
    TYPE_CHOICE = (('master_agent', 'Master Agent'),
                   ('import_agent', 'Import Agent'),
                   ('regular_agent', 'Regular Agent'),
                   )
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brand_agent')
    type = models.CharField(choices=TYPE_CHOICE, max_length=20)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='childs')
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.agency.name + " | " + self.brand.name

    def get_childs(self):
        return self.childs.all()
