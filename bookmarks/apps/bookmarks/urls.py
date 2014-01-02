# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import BookmarksListView, BookmarkCreateEditView, \
    BookmarkSearchView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url('^$', login_required(BookmarksListView.as_view()), name="main"),
    url('^save/$', login_required(BookmarkCreateEditView.as_view()), name="save"),
    url('^search/$', login_required(BookmarkSearchView.as_view()), name="search"),
)