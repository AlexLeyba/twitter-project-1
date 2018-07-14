# Generated by Django 2.0.7 on 2018-07-14 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField(default=0)),
                ('id_article', models.IntegerField(default=0)),
                ('like', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'user_likes',
            },
        ),
        migrations.CreateModel(
            name='UserMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateField()),
                ('text', models.CharField(max_length=250)),
                ('id_user', models.IntegerField(default=0)),
                ('total_likes', models.IntegerField(default=0)),
                ('retweet', models.BooleanField(default=False)),
                ('id_answer', models.IntegerField(default=0)),
                ('left', models.IntegerField(default=0)),
                ('right', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'user_messages',
            },
        ),
    ]
