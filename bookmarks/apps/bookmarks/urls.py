# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import BookmarksListView, BookmarkCreateEditView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url('^$', login_required(BookmarksListView.as_view()), name="main"),
    url('^add/$', login_required(BookmarkCreateEditView.as_view()), name="create"),
)