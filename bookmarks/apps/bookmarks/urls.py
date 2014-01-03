# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import BookmarksListView, BookmarkCreateEditView, \
    BookmarkSearchView, BookmarkVoteAPIView, BookmarkShareAPIView, \
    PopularListView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url('^$',
        view=login_required(BookmarksListView.as_view()),
        name='main'),
    url('^save/$',
        view=login_required(BookmarkCreateEditView.as_view()),
        name='save'),
    url('^popular/$',
        view=PopularListView.as_view(),
        name='popular'),
    url('^search/$',
        view=login_required(BookmarkSearchView.as_view()),
        name='search'),
    url('^ajax/vote/$',
        view=login_required(BookmarkVoteAPIView.as_view()),
        name='vote'),
    url('^ajax/share/$',
        view=login_required(BookmarkShareAPIView.as_view()),
        name='share'),
)