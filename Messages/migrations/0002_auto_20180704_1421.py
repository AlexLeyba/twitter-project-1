# Generated by Django 2.0.7 on 2018-07-04 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Messages', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_messages',
            new_name='UserMessages',
        ),
    ]
