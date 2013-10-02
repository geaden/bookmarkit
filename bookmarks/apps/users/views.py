# -*- coding: utf-8 -*-
import logging
import os
from apiclient.discovery import build
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.utils import timezone
from django.views.generic import FormView, CreateView, TemplateView, View
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
import httplib2
from oauth2client import xsrfutil
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage

from .forms import BookmarksAuthForm, BookmarkRegistrationForm, BookmarksPasswordResetForm
from .models import BookmarksUser, BookmarksUserManger, CredentialsModel


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class UserViewMixin:
    model = get_user_model()


class BookmarksAuthView(FormView):
    form_class = BookmarksAuthForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        if 'next' in self.request.GET:
            success_url = self.request.GET['next']
        else:
            success_url = settings.LOGIN_REDIRECT_URL
        return success_url

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
        return super(BookmarksAuthView, self).form_valid(form)


class BookmarksUserCreateView(UserViewMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = BookmarkRegistrationForm
    success_url = reverse_lazy('users:register-success')


class RegistrationConfirmView(TemplateView):
    """
    Registration confirm view
    """
    template_name = 'registration/registration_confirm.html'
    expired = False

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            ctx = super(RegistrationConfirmView, self).\
                get_context_data(**kwargs)
            ctx['has_account'] = True
            return ctx
        return super(RegistrationConfirmView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.object = BookmarksUser.objects.get(
            activation_key=kwargs['activation_key'])
        if self.object.key_expires < timezone.now():
            context['expired'] = True
            # Clean database
            self.object.delete()
        elif self.object.is_active:
            context['activated'] = True
        else:
            self.object.is_active = True
            self.object.save()
            context['created_user'] = self.object
        return self.render_to_response(context)


FLOW = OAuth2WebServerFlow(
    client_id=settings.GOOGLEAPI_CLIENT_ID,
    client_secret=settings.GOOGLEAPI_CLIENT_SECRET,
    scope='openid email profile',
    redirect_uri=settings.GOOGLEAPI_REDIRECT_URL)


class GoogleActivityView(TemplateView):
    """Test google view"""
    template_name = 'profiles/index.html'
    context = {}

    def get_context_data(self, **kwargs):
        ctx = super(GoogleActivityView, self).\
            get_context_data(**kwargs)
        ctx.update(self.context)
        return ctx

    def get(self, request, *args, **kwargs):
        storage = Storage(CredentialsModel,
                          'id', self.request.user.pk, 'credential')
        credential = storage.get()
        if credential is None or \
                credential.invalid:
            FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY,
                request.user)
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        else:
            http = httplib2.Http()
            http = credential.authorize(http)
            service = build("plus", "v1", http=http)
            activities = service.activities()
            activitylist = activities.list(collection='public',
                                           userId='me').execute()
            self.context['activitylist'] = activitylist
            logging.info(activitylist)
        return super(GoogleActivityView, self).\
            get(request, **kwargs)


class GoogleLoginView(View):
    """Google Login View"""
    def get(self, request, *args, **kwargs):
        storage = Storage(CredentialsModel,
                          'id', self.request.user.pk, 'credential')
        credential = storage.get()
        if credential is None or \
                credential.invalid:
            FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY,
                request.user)
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        else:
            HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super(GoogleLoginView, self).\
            get(request, **kwargs)


class BookmarksUserPasswordReset(FormView):
    form_class = BookmarksPasswordResetForm
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('bookmarks:main')

    def form_valid(self, form):
        user = self.request.user
        password = form.cleaned_data.get('password1')
        if password:
            user.set_password(password)
            user.save()
        return super(BookmarksUserPasswordReset, self).\
            form_valid(form)


class GoogleAuthReturnView(View):
    """Google Auth return view"""
    def get(self, request, **kwargs):
        if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.REQUEST['state'],
                request.user):
            return HttpResponseBadRequest()
        credential = FLOW.step2_exchange(request.REQUEST)
        user_document = self.get_user_info(credential)
        email = user_document['email']
        try:
            user = BookmarksUser.objects.get_by_natural_key(email)
        except BookmarksUser.DoesNotExist:
            user = None
        if user is not None:
            storage = Storage(CredentialsModel, 'id', user, 'credential')
            storage.put(credential)
            user = authenticate(google_user=user_document)
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        password = BookmarksUser.objects.make_random_password()
        user = BookmarksUser.objects.create_user(
            email=email,
            last_name=user_document['family_name'],
            first_name=user_document['given_name'],
            password=password)
        user_backend = authenticate(username=email,
                                    password=password)
        if user_backend:
            login(request, user_backend)
        if email == settings.ADMIN_USER:
            user.is_staff = True
            user.is_superuser = True
        user.gender = user_document['gender']
        user.birthday = user_document['birthday']
        user.picture = user_document['picture']
        user.google_id = user_document['id']
        user.save()
        storage = Storage(CredentialsModel, 'id', user, 'credential')
        storage.put(credential)
        return HttpResponseRedirect(reverse_lazy('users:reset'))

    def get_user_info(self, credential):
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("oauth2", "v2", http=http)
        user_document = service.userinfo().get().execute()
        return user_document

