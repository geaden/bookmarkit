# -*- coding: utf-8 -*-
from oauth2client.django_orm import FlowField, CredentialsField

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'

from django.db import models
from django.utils.translation import \
    ugettext_lazy as _

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)

# South
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^oauth2client\.django_orm\.FlowField"])
add_introspection_rules([], ["^oauth2client\.django_orm\.CredentialsField"])


class BookmarksUserManger(BaseUserManager):
    def create_user(self,
                    email,
                    last_name,
                    first_name,
                    password=None):
        """
        Creates and saves a User with
        the given email, last_name, first_name and password
        """
        if not email:
            msg = _('Users must have an email address')
            raise ValueError(msg)

        if not last_name and not first_name:
            msg = _('Users must have last and first name')
            raise ValueError(msg)

        user = self.model(
            email=BookmarksUserManger.normalize_email(email),
            last_name=last_name,
            first_name=first_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         last_name,
                         first_name,
                         password):
        """
        Creates and saves a superuser
        with the given email, last name,
        first name and password
        """
        user = self.create_user(email,
                                last_name=last_name,
                                first_name=first_name,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


USERNAME_FIELD = 'email'
REQUIRED_FIELDS = ['last_name', 'first_name',]

GENDER = (
    (u'male', _('Male')),
    (u'female', _('Female')),
)

nullable = {'null': True, 'blank': True}


class BookmarksUser(AbstractBaseUser, PermissionsMixin):
    """
    User for track finance
    """
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        db_index=True
    )
    last_name = models.CharField(_('Last name'), max_length=255)
    first_name = models.CharField(_('First name'), max_length=255)
    activation_key = models.CharField(max_length=40, blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, default=u'male')
    picture = models.URLField(**nullable)
    birthday = models.DateField(**nullable)
    google_id = models.CharField(max_length=255, **nullable)

    USERNAME_FIELD = USERNAME_FIELD
    REQUIRED_FIELDS = REQUIRED_FIELDS

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    objects = BookmarksUserManger()

    def get_full_name(self):
        """
        The user is identified by their email,
        last and first name
        """
        return u'{first_name} {last_name} ({email})'.format(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email
        )

    def get_short_name(self):
        """
        The user is identified by their email
        """
        return self.email

    def __unicode__(self):
        return self.email


class FlowModel(models.Model):
    """Model for OAuth2"""
    id = models.ForeignKey(BookmarksUser, primary_key=True)
    flow = FlowField()


class CredentialsModel(models.Model):
    """Credentials for OAuth2"""
    id = models.ForeignKey(BookmarksUser, primary_key=True)
    credential = CredentialsField()

