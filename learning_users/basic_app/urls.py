from django.conf.urls import url
from basic_app import views

#Template tagging
app_name = 'basic_app'

urlpatterns = [
    url(r'^login/$', views.user_login, name = 'user_login'),
    url(r'^special/$', views.special, name = 'special'),
    url(r'^registration/$', views.registration, name = 'registration'),
]
