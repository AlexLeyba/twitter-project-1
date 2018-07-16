from Libraries import *


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


def calculate_likes():
    all_likes = UserMessages.objects.all()
    for e in all_likes:
        try:
            number = Likes.objects.filter(id_article=e.id, like=True).count()
        except:
            number = 0
        e.total_likes = number
        e.save()


def get_conf_likes(request):
    array=[]
    all_articles = UserMessages.objects.filter(~Q(id_user=0))
    for e in all_articles:
        try:
            obj = Likes.objects.get(id_article=e.id, id_user=request.user.id)
            array.append(obj.like)
        except:
            array.append(False)

    return array


def get_edit_art(request):
    array = []
    all_articles = UserMessages.objects.filter(~Q(id_user=0))
    id_user = request.user.id
    for e in all_articles:
        if e.id_user != id_user and request.user.is_authenticated == True:
            array.append(True)
        else:
            array.append(False)

    return array


def create_message(request, answer, mess, id_article):
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