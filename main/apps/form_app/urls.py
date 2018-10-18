from django.conf.urls import url, include
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^pizzas/$', views.create),
    url(r'^login/$', views.login),
]