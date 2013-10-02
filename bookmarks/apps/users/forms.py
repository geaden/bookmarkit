# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django import forms
from django.contrib.auth.hashers import UNUSABLE_PASSWORD
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.mail import send_mail
from django.forms import TextInput, PasswordInput
from django.template import loader
from django.utils import timezone
from django.utils.http import int_to_base36
from django.utils.translation import \
    ugettext_lazy as _

from captcha.fields import ReCaptchaField

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


decoration = lambda x: {'class': 'form-control',
                        'placeholder': x}


class BookmarksAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(
        attrs=decoration(_('Email'))))
    password = forms.CharField(widget=PasswordInput(
        attrs=decoration(_('Password'))))


class BookmarksPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        User = get_user_model()
        email = self.cleaned_data['email']
        self.users_cache = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages[u'unknown'])
        if any(user.password == UNUSABLE_PASSWORD for user in self.users_cache):
            raise forms.ValidationError(self.error_messages[u'unusable'])
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject=subject,
                      message=email,
                      from_email=None,
                      recipient_list=(user.email,))


class BookmarkRegistrationForm(UserCreationForm):
    username = forms.EmailField(max_length=75,
                                widget=TextInput(attrs=decoration(_('Email'))))
    last_name = forms.CharField(max_length=180,
                                widget=TextInput(attrs=decoration(_('Last name'))))
    first_name = forms.CharField(max_length=180,
                                 widget=TextInput(attrs=decoration(_('First name'))))
    password1 = forms.CharField(max_length=180,
                                widget=TextInput(attrs=decoration(_('Password'))))
    password2 = forms.CharField(max_length=180,
                                widget=TextInput(attrs=decoration(_('Confirm password'))))
    captcha = ReCaptchaField(attrs={'theme': 'clean'})

    class Meta:
        model = get_user_model()
        fields = ('last_name', 'first_name',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            self.Meta.model.objects.get(email=username)
        except self.Meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages[u'duplicate_username'])

    def save(self, commit=True):
        user = super(BookmarkRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['username']
        user.set_password(self.cleaned_data["password1"])
        user.activation_key = default_token_generator.\
            make_token(user)
        user.key_expires = timezone.now() + datetime.timedelta(days=2,)
        user.is_active = False
        current_site = get_current_site(None)
        site_name = current_site.name
        domain = current_site.domain
        use_https = False
        c = {
            'email': user.email,
            'site_name': site_name,
            'domain': domain,
            'user': user,
            'activation_key': user.activation_key,
            'expires': user.key_expires,
            'protocol': use_https and 'https' or 'http'
        }
        email_subject = _('Confirm your Bookmark.It account')
        email_body = loader.render_to_string(
            'registration/registration_confirm_email.html',
            c
        )
        if commit:
            user.save()
            send_mail(subject=email_subject,
                      message=email_body,
                      from_email=None,
                      recipient_list=(user.email,))
        return user


class BookmarksPasswordResetForm(forms.Form):
    password1 = forms.CharField(required=True, widget=PasswordInput(
        attrs=decoration(_('New password'))))
    password2 = forms.CharField(required=True, widget=PasswordInput(
        attrs=decoration(_('Password again'))))

    def clean(self):
        cleaned_data = super(BookmarksPasswordResetForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2:
            if not password1 == password2:
                raise forms.ValidationError(_('Passwords do not match. Please check.'))
        return super(BookmarksPasswordResetForm, self).clean()