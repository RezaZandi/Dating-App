# Generated by Django 2.2.3 on 2020-04-26 20:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0011_auto_20200426_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instantmessage',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 26, 20, 7, 20, 777400, tzinfo=utc), verbose_name='Data creation'),
        ),
    ]
