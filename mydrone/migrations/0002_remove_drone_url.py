# Generated by Django 3.2.4 on 2021-10-26 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mydrone', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drone',
            name='url',
        ),
    ]
