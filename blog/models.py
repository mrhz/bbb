import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from hitcount.models import HitCountMixin, HitCount
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from buildino import settings


class PageCount(models.Model, HitCountMixin):
    page_name = models.CharField(max_length=150, help_text="Enter the page name that want hitcounter on it. ")
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.page_name


class Category(models.Model):
    title = models.CharField(max_length=150, help_text="Enter a Category Name")
    slug = models.SlugField(max_length=200, help_text="Category URL")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now, )
    last_update = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        str=""
        if self.parent:
            str += self.parent.title + " >> "
        return  str + self.title

    class Meta:
        ordering = ("title",)

    def save(self, *args, **kwargs):
        # Raise on circular reference
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise RuntimeError("Circular references not allowed")
            parent = parent.parent

        super(Category, self).save(*args, **kwargs)



    @property
    def children(self):
        return self.category_set.all().order_by('title')
    # get_absolute_url


class Tag(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=50)
    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# if you use persian name for file names its rise an error so to fix this problem we change name after save
def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    date = timezone.now()
    return "%s%s/%s.%s" % (date.year,date.month,uuid.uuid4(), extension)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Article(models.Model, HitCountMixin):
    STATUS_CHOICE = (('draft', 'Draft'),
                     ('archived', 'Archived'),
                     ('published', 'Published'),
                     ('hidden', 'Hidden'),
                     )
    title = models.CharField(max_length=255)
    card_image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    card_image_thumbnail = ImageSpecField(source='card_image',
                                          processors=[ResizeToFill(1200, 500)],
                                          format='JPEG',
                                          options={'quality': 90})
    card_image_featured_thumbnail = ImageSpecField(source='card_image',
                                          processors=[ResizeToFill(300, 300)],
                                          format='JPEG',
                                          options={'quality': 90})

    main_image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    main_image_thumbnail = ImageSpecField(source='main_image',
                                          processors=[ResizeToFill(1280, 500)],
                                          format='JPEG',
                                          options={'quality': 90})
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    trashed = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True, max_length=255, unique=True, allow_unicode=True, help_text="Used to Create Post's URL")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='draft')
    publish_date = models.DateTimeField(default=timezone.now, help_text="It's Article Publish Date")
    creation_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    start_publish_date = models.DateTimeField(blank=True, null=True, help_text='Start Date of a Publication')
    end_publish_date = models.DateTimeField(blank=True, null=True, help_text='End Date of a Publication')
    tags = models.ManyToManyField(Tag, blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    # tags
    # categories

    objects = models.Manager()
    published = PublishedManager()



    class Meta:
        ordering = ("-publish_date",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.publish_date.year,
                                               self.publish_date.month,
                                               self.publish_date.day,
                                               self.slug, ])

    def get_hitcount(article):
        obj = HitCount.objects.get_for_object(article)
        hit_count = obj.hits
        return hit_count



class MetaData(models.Model):
    keyword = models.CharField(null=True, blank=True, max_length=8000)
    description = models.CharField(null=True, blank=True, max_length=8000)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.keyword


def create_slug(instance, new_slug = None):
    # slug = slugify(instance.title)
    # slugify dont work for persian characters! so we use code below
    slug = instance.title
    slug = slug.replace(" ", "-")
    slug = slug.replace("،", "-")
    slug = slug.replace(")", "")
    slug = slug.replace("(", "")
    slug = slug.replace("؟", "")
    slug = slug.replace(".", "")
    slug = slug.replace(":", "")
    slug = slug.replace(";", "")
    slug = slug.replace(",", "")
    slug = slug.replace("‌", "-")
    slug = slug.replace("‌<<", "-")
    slug = slug.replace(">>", "-")
    slug = slug.replace("؛", "-")
    slug = slug.replace("?", "")
    slug = slug.replace("!", "")
    slug = slug.replace("'", "")
    slug = slug.replace('"', "")
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug)
    if qs.exists():
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciver, sender=Article)
