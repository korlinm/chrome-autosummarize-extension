from django.urls import path
from django.conf.urls import url
from django.urls import include, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^get_wiki_summary/$', views.get_wiki_summary, name='get_wiki_summary'),
    url(r'^get_page_summary/$', views.get_page_summary, name='get_page_summary'),
]
