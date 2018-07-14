from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UserMessages(models.Model):
    creation_time = models.DateField()
    text = models.CharField(max_length=250)
    id_user = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    retweet = models.BooleanField(default=False)
    id_answer = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    right = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=12)
    object_id = models.PositiveIntegerField(default=1)

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'user_messages'


class Trees(models.Model):
    tree_name = models.CharField(max_length=100)


class Likes(models.Model):
    id_user = models.IntegerField(default=0)
    id_article = models.IntegerField(default=0)
    like = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_likes'


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


class Album(models.Model):
    # artist = models.ForeignKey(Musician, on_delete=models.CASCADE, to_field='id')
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default='')

    content_object = GenericForeignKey('content_type', 'object_id')
    # def get_mus_first_name(self):
    #     name = Musician.objects.get(id=self.artist_id).first_name
    #     return name