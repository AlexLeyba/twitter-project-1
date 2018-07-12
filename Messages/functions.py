from django.shortcuts import render, redirect, HttpResponse
from Messages.models import UserMessages, Likes
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from _datetime import datetime
import asyncio
from django.db import connection
from django.db.models import Q, Max


def add_new_message(request, text_message, id_answer):
    date = datetime.now().date()
    all = UserMessages.objects.filter(~Q(id_user=0))
    id = request.user.id
    right = int(all.aggregate(Max('right'))['right__max']) + 2
    left = right - 1
    if id_answer != 0:
        retweet = True
    else:
        retweet = False

    i = UserMessages.objects.create(creation_time=date, text=text_message,
                                    id_user=id, total_likes=0, retweet=retweet,
                                    left=left, right=right)
    i.save()
    user = UserMessages.objects.get(id_user=0)
    user.right = user.right + 2
    user.save()


def is_int(letter):
    for x in range(10):
        if letter == str(x):
            return 'achtung'
    return 'pass'


async def send_email(request, email, user):
    subject = 'Thank you'
    message = 'http://127.0.0.1:8000/email_conf/' + str(user) + '/'
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, message, from_email, to_list, fail_silently=False)
    return HttpResponse('Message was sent to your email!')

