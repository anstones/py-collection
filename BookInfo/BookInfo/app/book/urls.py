#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^books/$', views.BooksAPIVIew.as_view()),
    # url(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view())
]