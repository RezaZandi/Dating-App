# Generated by Django 2.2.3 on 2020-05-11 01:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0015_auto_20200503_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instantmessage',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data creation'),
        ),
    ]