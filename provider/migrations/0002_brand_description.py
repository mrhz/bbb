# Generated by Django 2.1.1 on 2018-09-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
