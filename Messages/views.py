from Messages.functions import *


def main_page(request, page_number=1):
    attention = ''
    calculate_likes()
    like = get_conf_likes(request)
    edit = get_edit_art(request)
    all = UserMessages.objects.filter(~Q(id_user=0))

    obj_list = get_big_arr(like, edit, all)
    current_page = Paginator(obj_list, 4)

    if request.user.is_authenticated:
        text_message = request.GET.get('text_message', '')
        if text_message != '':
            if len(text_message) >= 250:
                attention = 'achtung'
                context = {'articles': current_page.page(page_number), 'attention': attention}
                return render(request, 'main/index.html', context)
            else:
                add_new_message(request, text_message)

    context = {'articles': current_page.page(page_number), 'attention': attention}
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


def user_retweet(request, id_article, id_creater):
    user = str(request.user)
    mess = UserMessages.objects.get(id=id_article, id_user=id_creater)
    text_message = 'User ' + user + ' retweeted: "' + mess.text + '"'
    add_new_message(request, text_message, id_article)
    return redirect('/')


def message(request, id_article):
    answer = request.GET.get('answer', '')
    mess = UserMessages.objects
    cursor = connection.cursor()
    left = mess.filter(id_answer=id_article).aggregate(Max('left'))['left__max']

    if left == None:
        left = mess.filter(id=id_article).aggregate(Max('left'))['left__max']

    if answer != '' and len(answer) <= 250:
        id_article = int(id_article)
        date = datetime.now().date()
        id_user = request.user.id
        num = int(left) + 1
        cursor.execute("UPDATE `user_messages` SET `left` = `left` + 2 WHERE `left` >= " + str(num))
        cursor.execute("UPDATE `user_messages` SET `right` = `right` + 2 WHERE `right` >= " + str(num))

        mess.create(creation_time=date, text=answer, id_user=id_user,
                    total_likes=0, retweet=False, id_answer=id_article,
                    left=left + 1, right=left + 2)

    mes = mess.get(id=id_article)

    left = mes.left
    right = mes.right

    if mes.id_answer != 0:
        left_add = left - 1
        text_message = mess.get(left=left_add).text
        id_user = mess.get(left=left_add).id_user
        user_name = User.objects.get(id=id_user).username

        cursor.execute("SELECT ms.id, ms.text, us.username " +
                       "FROM twitter.user_messages AS ms " +
                       "INNER JOIN twitter.auth_user AS us ON ms.id_user = us.id " +
                       "WHERE ms.id_answer=" + str(id_article) +
                       " AND ms.left > " + str(left) +
                       " AND ms.right < " + str(right))

        answer_to_message = mess.get(id=id_article).text
        id_user = mess.get(id=id_article).id_user
        answer_to_username = User.objects.get(id=id_user).username

    else:
        cursor.execute("SELECT ms.id, ms.text, us.username " +
                       "FROM twitter.user_messages AS ms " +
                       "INNER JOIN twitter.auth_user AS us ON ms.id_user = us.id " +
                       "WHERE ms.id_answer=" + str(id_article) +
                        " AND ms.left > " + str(left) +
                        " AND ms.right < " + str(right))
        text_message = mess.get(id=id_article).text
        id_user = mess.get(id=id_article).id_user
        user_name = User.objects.get(id=id_user).username
        answer_to_message=''
        answer_to_username=''

    if user_name == '':
        user_name = 'Anonimus'

    context = {
        'message': text_message,
        'username': user_name,
        'answer_to_message': answer_to_message,
        'answer_to_username': answer_to_username,
        'cursor': cursor,
    }

    if answer != '':
        return redirect('http://127.0.0.1:8000/message/' + str(id_article))
    else:
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
