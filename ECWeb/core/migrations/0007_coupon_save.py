# Generated by Django 2.2.12 on 2020-05-13 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200513_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='save',
            field=models.FloatField(default=20),
        ),
    ]
