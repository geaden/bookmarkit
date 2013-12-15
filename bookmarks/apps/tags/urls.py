# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import TagAutocompleteView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url(r'^autocomplete/$',
        view=login_required(TagAutocompleteView.as_view()),
        name='autocomplete'),
)