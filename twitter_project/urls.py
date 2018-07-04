from django.contrib import admin
from django.urls import path, include
from Messages import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('admin/', admin.site.urls),
    path('', include('Messages.urls')),

]
