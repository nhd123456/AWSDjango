# Generated by Django 3.0.6 on 2020-05-22 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_blog_images_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog_images',
            name='mentioned_item',
            field=models.ManyToManyField(to='core.Item'),
        ),
    ]
