from django.db import models


class UserMessages(models.Model):
    creation_time = models.DateField()
    text = models.CharField(max_length=250)

    class Meta:
        db_table = 'user_messages'
