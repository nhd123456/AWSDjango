# Generated by Django 3.0.6 on 2020-05-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20200522_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='intro_image',
            field=models.ManyToManyField(blank=True, related_name='img', to='core.item_image'),
        ),
    ]
