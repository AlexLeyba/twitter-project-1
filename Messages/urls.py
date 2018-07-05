from django.contrib import admin
from django.urls import path, include, re_path
from Messages import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
    re_path('^page/(\d+)/$', views.main_page),
    # path('test/', views.test),
    re_path('^email_conf/(?P<user>)\w+/$', views.check_from_email)
]