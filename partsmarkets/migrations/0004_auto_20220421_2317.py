# Generated by Django 3.2.12 on 2022-04-21 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_my_equips'),
        ('partsmarkets', '0003_auto_20220418_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='name',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.equipgroup'),
        ),
    ]
