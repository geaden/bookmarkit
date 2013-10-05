# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from .views import FolderListCreateView, FolderRetrieveUpdateDestroyView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url(r'^$', FolderListCreateView.as_view(), name='list_create'),
    url(r'^(?P<pk>\d+)$', FolderRetrieveUpdateDestroyView.as_view(),
        name='retrieve_update_destroy'),
)