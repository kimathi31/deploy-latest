from django.urls import path
from django.contrib import admin
from detectapi import views
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('detect', views.deploy, name = 'detect'),
    path('getdata',views.getdata,name = 'getdata'),
    
    
]