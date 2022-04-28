# Generated by Django 3.2.12 on 2022-04-28 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualpools', '0003_remove_stockinfo_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compatibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('group', models.ManyToManyField(blank=True, to='virtualpools.Stock')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
