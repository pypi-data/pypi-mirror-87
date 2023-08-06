from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'financial'
urlpatterns = [
    path('req/', request, name='request'),
    path('req-test/', testzb, name='request'),
    path('callback/', testback, name='callback'),

]
