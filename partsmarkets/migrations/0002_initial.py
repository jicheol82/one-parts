# Generated by Django 3.2.12 on 2022-04-03 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('partsmarkets', '0001_initial'),
        ('virtualpools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.equipgroup'),
        ),
        migrations.AddField(
            model_name='product',
            name='maker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='virtualpools.officialmakername'),
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='partsmarkets.product'),
        ),
    ]