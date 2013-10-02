# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from .views import FriendAcceptView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url(r'^accept/(?P<code>\w+)/?$',
        FriendAcceptView.as_view(), name='accept'),
)