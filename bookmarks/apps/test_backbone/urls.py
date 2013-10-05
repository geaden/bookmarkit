# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from .views import AppView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url('^$', AppView.as_view(), name='main')
)

