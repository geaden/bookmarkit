# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import BookmarksAuthView, BookmarksUserCreateView, RegistrationConfirmView, \
    GoogleActivityView, GoogleLoginView, BookmarksUserPasswordReset, GoogleAuthReturnView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns('',
                       url(r'^login/?$', BookmarksAuthView.as_view(), name='login'),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           name='logout'),
                       url(r'^register/$',
                           BookmarksUserCreateView.as_view(),
                           name='register'),
                       url(r'^register/created/',
                           TemplateView.as_view(
                                template_name='registration/register_created.html'),
                           name='register-success'),
                       url(r'^register/confirm/(?P<activation_key>[a-z0-9-]+)$',
                           RegistrationConfirmView.as_view(),
                           name='registration-confirm'),
                       url(r'^login/google/?$', GoogleLoginView.as_view(), name='google'),
                       url(r'^activity/?$', GoogleActivityView.as_view(), name='activity'),
                       url(r'^oauth2callback', GoogleAuthReturnView.as_view(), name='oauth'),
                       url(r'^reset', login_required(
                           BookmarksUserPasswordReset.as_view()), name='reset'),
                       )