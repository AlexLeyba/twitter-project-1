from django.db import models


class UserMessages(models.Model):
    creation_time = models.DateField()
    text = models.CharField(max_length=250)
    id_user = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_messages'


class Likes(models.Model):
    id_user = models.IntegerField(default=0)
    id_article = models.IntegerField(default=0)
    like = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_likes'
