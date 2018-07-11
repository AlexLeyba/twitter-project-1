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


def main_page(request, page_number=1):
    attention = ''
    calculate_likes()
    like = get_conf_likes(request)
    edit = get_edit_art(request)
    all = UserMessages.objects.all()

    obj_list = get_big_arr(like, edit, all)
    current_page = Paginator(obj_list, 2)
    print(current_page)
    context = {'articles': current_page.page(page_number), 'attention': attention}
    if request.user.is_authenticated:
        text_message = request.GET.get('text_message', '')
        if text_message != '':
            if len(text_message) >= 250:
                attention = 'achtung'
                context = {'articles': current_page.page(page_number), 'attention': attention}
                return render(request, 'main/index.html', context)
            else:
                date = datetime.now().date()
                id = request.user.id
                i = UserMessages.objects.create(creation_time=date, text=text_message, id_user=id, total_likes=0, retweet=False)
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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_email(request, email, user))
        loop.close()
        return HttpResponse('Message was sent to your email!')
    return render(request, 'main/registration.html')


async def send_email(request, email, user):
    subject = 'Thank you'
    message = 'http://127.0.0.1:8000/email_conf/' + str(user) + '/'
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, message, from_email, to_list, fail_silently=False)
    return HttpResponse('Message was sent to your email!')


def check_from_email(request, user):
    user = User.objects.get(username=user)
    user.is_active = 1
    user.save()
    return redirect('login')


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


def user_add_like(request, id_article):
    if request.user.is_authenticated:
        try:
            id_u = request.user.id
            i = Likes.objects.get(id_user=id_u, id_article=id_article)
            if not i.like:
                i.like = True
            else:
                i.like = False
            i.save()
        except:
            Likes.objects.create(id_user=id_u, id_article=id_article, like=True)
    return redirect('/')


def calculate_likes():
    all_likes = UserMessages.objects.all()
    for e in all_likes:
        try:
            number = Likes.objects.filter(id_article=e.id, like=True).count()
            e.total_likes = number
            e.save()
        except:
            number = 0
            e.total_likes = number
            e.save()


def get_conf_likes(request):
    array=[]
    all_articles = UserMessages.objects.all()
    for e in all_articles:
        try:
            obj = Likes.objects.get(id_article=e.id, id_user=request.user.id)
            array.append(obj.like)
        except:
            array.append(False)

    return array


def get_edit_art(request):
    array=[]
    all_articles = UserMessages.objects.all()
    id_user = request.user.id
    for e in all_articles:
        if e.id_user != id_user and request.user.is_authenticated == True:
            array.append(True)
        else:
            array.append(False)

    return array


def get_big_arr(like, edit, all):
    main_array = []
    for e in range(len(like)):
        array = []
        array.append(all[e].text)
        array.append(all[e].id)
        array.append(all[e].id_user)
        array.append(like[e])
        array.append(edit[e])
        array.append(all[e].total_likes)
        array.append((all[e].retweet))
        main_array.append(array)

    return main_array


def user_retweet(request, id_article, id_creater):
    id_user = request.user.id
    user = str(request.user)
    date = datetime.now().date()
    mess = UserMessages.objects.get(id=id_article, id_user=id_creater)
    text = 'User ' + user + ' retweeted: "' + mess.text +'"'
    i = UserMessages.objects.create(creation_time=date, text=text, id_user=id_user, total_likes=0, retweet=True)
    i.save()
    return redirect('/')


def message(request, id_article):
    answer = request.GET.get('answer', '')
    mess = UserMessages.objects
    if answer != '' and len(answer) <= 250:
        id_article = int(id_article)
        date = datetime.now().date()
        id_user = request.user.id
        mess.create(creation_time=date, text=answer, id_user=id_user, total_likes=0, retweet=False, id_answer=id_article)

    left = mess.get(id=id_article).left
    right = mess.get(id=id_article).right
    cursor = connection.cursor()
    cursor.execute("SELECT ms.id, ms.text, us.username " +
                   "FROM twitter.user_messages AS ms " +
                   "INNER JOIN twitter.auth_user AS us ON ms.id_user = us.id " +
                   "WHERE ms.id_answer=" + str(id_article) +
                    " AND ms.left > " + str(left) +
                    " AND ms.right < " + str(right))

    text_message = mess.get(id=id_article).text
    id_user = mess.get(id=id_article).id_user
    user_name = User.objects.get(id=id_user).username

    if user_name == '':
        user_name = 'Anonimus'

    context = {
        'message': text_message,
        'username': user_name,
        'cursor': cursor,
    }
    return render(request, 'main/message.html', context)


def profile(request, id_user):
    first_letter = ''
    field_name = request.GET.get('name', '')
    user = User.objects.get(id=id_user)
    username = user.username

    if field_name != '':
        first_letter = is_int(field_name[0])
        if first_letter != 'achtung':
            user.username = field_name
            user.save()

    context = {
        'name': username,
        'attention': first_letter,
    }
    return render(request, 'main/profile.html', context)


def is_int(letter):
    for x in range(10):
        if letter == str(x):
            return 'achtung'
    return 'pass'
# async def say(what, when):
#     # await asyncio.sleep(when)
#     print(what)
#
# def test(request):
#     # Group.objects.create(name='users')
#     # Group.objects.create(name='admin')
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(say('hello', 0))
#     loop.close()
#     return render(request, 'test.html')



