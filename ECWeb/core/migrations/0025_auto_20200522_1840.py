# Generated by Django 3.0.6 on 2020-05-22 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200522_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='intro_image',
            field=models.ManyToManyField(blank=True, to='core.item_image'),
        ),
    ]
