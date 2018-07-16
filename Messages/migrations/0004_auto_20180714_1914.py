# Generated by Django 2.0.7 on 2018-07-14 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('Messages', '0003_trees'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessages',
            name='content_type',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='usermessages',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
        ),
    ]