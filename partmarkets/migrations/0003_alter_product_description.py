# Generated by Django 3.2.12 on 2022-04-02 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partmarkets', '0002_auto_20220402_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
