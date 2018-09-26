from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.utils import timezone
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from activity.models import Activity
from blog.models import upload_location
from provider.models import Reseller, Agency


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Type(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=300)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=300)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=240)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, blank=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    quality_degree = models.CharField(max_length=100, blank=True)
    # slug = models.SlugField()
    reseller = models.ForeignKey(Reseller, on_delete=models.PROTECT)
    related_to = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, )
    type = models.ForeignKey(Type, related_name='products', on_delete=models.CASCADE, )
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)  # Deprecated
    is_available = models.BooleanField(default=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)
    favorite = GenericRelation(Activity)

    def __str__(self):
        return self.name

    def clean(self):
        if self.reseller.brand.status != "accepted":
            raise ValidationError('برند غیر فعال است')
        super(Product, self).clean()

    def save(self, *args, **kwargs):
        if self.reseller.brand.status != "accepted":
            raise ValidationError('برند غیر فعال است')
        super(Product, self).save(*args, **kwargs)


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    img = models.ImageField(upload_to=upload_location, null=True, blank=True)
    img_thumbnail = ImageSpecField(source='img',
                                          processors=[ResizeToFill(500, 500)],
                                          format='JPEG',
                                          options={'quality': 90})
    img_product = ImageSpecField(source='img',
                                          processors=[ResizeToFill(700, 900)],
                                          format='JPEG',
                                          options={'quality': 90})
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + '| media'


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0.00, blank=True)
    inherit_unit_price = models.BooleanField(default=False,)
    tax = models.IntegerField(default=0, blank=True)
    inherit_tax = models.BooleanField(default=False, )
    discount = models.IntegerField(default=0, blank=True, null=True)
    inherit_discount = models.BooleanField(default=True,)
    is_available = models.BooleanField(default=True, blank=True)
    inherit_availability = models.BooleanField(default=True)
    is_tax_included = models.BooleanField(default=False,  blank=True)
    inherit_tax_included = models.BooleanField(default=True,)
    proposed_by = models.ForeignKey(Agency, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return "Price of " + self.product.name + " by " + self.proposed_by.name



class Field(models.Model):
    name = models.CharField(max_length=100)
    TYPE = (
        ('char', 'Character'),
        ('txt', 'Text'),
        ('int', 'Integer'),
        ('flo', 'Float'),
        ('dat', 'Date'),
        ('datt', 'DateTime'),
        ('img', 'Image'),
        ('fle', 'File'),
    )
    type_choice = models.CharField(max_length=120, choices=TYPE)
    type_field = models.ForeignKey(Type, on_delete=models.PROTECT)

    def __str__(self):
        return self.name + " | " + self.type_field.name


class ProductField(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    field = models.ForeignKey(Field, on_delete=models.PROTECT)

    char_field = models.CharField(max_length=100000, null=True, blank=True)
    text_field = models.TextField(null=True, blank=True)
    int_field = models.IntegerField(null=True, blank=True)
    big_int_field = models.BigIntegerField(null=True, blank=True)
    float_field = models.FloatField(null=True, blank=True)
    date_field = models.DateField(default=timezone.now)
    date_time_field = models.DateTimeField(null=True, blank=True)
    image_field = models.ImageField(upload_to=upload_location, blank=True, null=True)
    file_field = models.FileField(upload_to=upload_location, blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=100)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return self.product.name + " | " + self.field.name

    def set_field_value(self, value):
        if self.field.type_choice == 'txt':
            self.text_field = value
        elif self.field.type_choice == "char":
            self.char_field = value
        elif self.field.type_choice == "int":
            self.int_field = value
        elif self.field.type_choice == "flo":
            self.float_field = value
        elif self.field.type_choice == "dat":
            self.date_field = value
        elif self.field.type_choice == "datt":
            self.date_time_field = value
        elif self.field.type_choice == "img":
            self.image_field = value
        elif self.field.type_choice == "fle":
            self.file_field = value

    @property
    def product_field(self):
        if self.field.type_choice == 'txt':
            return self.text_field
        elif self.field.type_choice == "char":
            return self.char_field
        elif self.field.type_choice == "int":
            return self.int_field
        elif self.field.type_choice == "flo":
            return self.float_field
        elif self.field.type_choice == "dat":
            return self.date_field
        elif self.field.type_choice == "datt":
            return self.date_time_field
        elif self.field.type_choice == "img":
            return self.image_field
        elif self.field.type_choice == "fle":
            return self.file_field
        else:
            return "omg!!!"



