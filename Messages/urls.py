from django.contrib import admin
from django.urls import path, include, re_path
from Messages import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
    re_path('^page/(\d+)/$', views.main_page),
    re_path('^email_conf/(?P<user>\w+)/$', views.check_from_email),
    re_path('^user/(?P<id_us>\w+)/$', views.user_messages, name='user_messages'),
    re_path('^user_edit/(?P<id_us>\w+)/(?P<ed>\w+)/(?P<id_article>\w+)/$', views.user_messages_edit, name="user_edit"),
    re_path('^user_add_like/(?P<id_article>\w+)/$', views.user_add_like, name="user_add_article"),
    re_path('^user_retweet/(?P<id_article>\w+)/(?P<id_creater>\w+)/$',views.user_retweet, name="user_retweet"),
    # path('test/', views.test),
]