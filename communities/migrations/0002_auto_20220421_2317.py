# Generated by Django 3.2.12 on 2022-04-21 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='name',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='name',
        ),
    ]
