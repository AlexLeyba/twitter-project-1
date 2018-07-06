from django.shortcuts import render, redirect, HttpResponse
from Messages.models import UserMessages
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
import subprocess


def main_page(request, page_number=1):
    attention = ''
    all_articles = UserMessages.objects.all()
    current_page = Paginator(all_articles, 2)
    context = {'articles': current_page.page(page_number), 'attention': attention}
    if request.user.is_authenticated:
        text_message = request.GET.get('text_message', '')
        if text_message != '':
            if len(text_message) >= 250:
                attention = 'achtung'
                context = {'articles': current_page.page(page_number), 'attention': attention}
                return render(request, 'main/index.html', context)
            else:
                date = datetime.datetime.now().date()
                id = request.user.id
                i = UserMessages.objects.create(creation_time=date, text=text_message, id_user=id)
                i.save()

    return render(request, 'main/index.html', context)


def user_login(request):
    if not request.user.is_authenticated:
        name = request.GET.get('user_value', '')
        pasw = request.GET.get('pass_value', '')
        user = authenticate(username=name, password=pasw)

        if user is not None:
            group = User.objects.get(username=name).groups.get()
            if user.is_active == 1 and str(group) == 'users':
                login(request, user)
                return redirect('main')
            else:
                return render(request, 'main/login.html')
        else:
            return render(request,'main/login.html')
    else:
        return redirect('main')


def user_logout(request):
    logout(request)
    return redirect('main')


def user_registration(request):
    user = request.GET.get('user_value','')
    pasw = request.GET.get('pass_value','')
    email = request.GET.get('email_value','')
    if user != '' and pasw != '' and email != '':
        user = User.objects.create_user(user, email, pasw, is_active=0)
        group = Group.objects.get(name='users')
        User.objects.get(username=user).groups.add(group)
        user.save()
        send_email(request, email, user)
        return HttpResponse('Message was sent to your email!')
    return render(request, 'main/registration.html')


def send_email(request, email, user):
    subject = 'Thank you'
    message = 'http://127.0.0.1:8000/email_conf/' + user + '/'
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, message, from_email, to_list)
    return HttpResponse('Message was sent to your email!')


def check_from_email(request, login):
    user = User.objects.get(username=login)
    user.is_active = 1
    user.save()
    return render(request, 'login')


def user_messages(request, id_us, ed=False):
    all_articles = UserMessages.objects.filter(id_user=id_us)

    context = {
        'articles': all_articles,
        'edit': ed
    }
    return render(request, 'main/user_page.html', context)


def user_messages_edit(request, id_us, ed=True, id_article=None):
    text = request.GET.get('change_message', '')
    if text != '':
        art = UserMessages.objects.get(id=id_article)
        art.text = text
        art.save()
    all_articles = UserMessages.objects.filter(id_user=id_us)
    text_message = UserMessages.objects.filter(id=id_article).values_list()
    context = {
        'articles': all_articles,
        'edit': ed,
        'id_article': id_article,
        'text_message': text_message[0][2]
    }
    return render(request, 'main/user_page.html', context)

# def test(request):
#     # Group.objects.create(name='users')
#     # Group.objects.create(name='admin')
#     return render(request, 'test.html')