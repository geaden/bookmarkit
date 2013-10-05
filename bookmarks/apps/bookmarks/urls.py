# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import BookmarksListView, BookmarkCreateView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url(r'^$', login_required(BookmarksListView.as_view()), name="main"),
    url(r'^add/$', login_required(BookmarkCreateView.as_view()), name="create"),
)