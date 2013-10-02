# -*- coding: utf-8 -*-

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from ..users.models import BookmarksUser


class BookmarksUserCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    Includes all the required fields, plus a repeated password.
    """
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput
    )

    class Meta:
        models = BookmarksUser
        fields = (
            'email',
            'last_name',
            'first_name'
        )

    def clean_password2(self):
        """
        Checks that two passwords entries match
        """
        data = self.cleaned_data
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 and \
            password2 and \
                password1 != password2:
            msg = _('Passwords don\'t match')
            raise forms.ValidationError(msg)

        return password2

    def save(self, commit=True):
        """
        Saves the provided password in hashed format
        """
        user = super(BookmarksUser, self).save(commit=False)
        data = self.cleaned_data
        user.set_password(data['password1'])
        if commit:
            user.save()
        return user


class BookmarksUserChangeForm(forms.ModelForm):
    """
    A form for updating users.

    Includes all the fields on the user, but replaces the
    password field with admin's password hash display field
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = BookmarksUser

    def clean_password(self):
        """
        Regardless of what the user provides, return
        the initial value.
        """
        return self.initial['password']


class BookmarksUserAdmin(UserAdmin):
    """
    Set the add/modify forms
    """
    add_form = BookmarksUserCreationForm
    form = BookmarksUserChangeForm

    list_display = ('email',
                    'is_staff')

    list_filter = ('is_staff',
                   'is_superuser',
                   'is_active',
                   'groups'
    )

    search_fields = ('email',
                     'last_name'
    )

    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('email',
                           'password',)}),

        (_('Personal info'), {'fields': ('last_name',
                                        'first_name',
        )}),

        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),

        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'last_name',
                       'first_name',
                       'password1',
                       'password2'
            )
        })
    )

admin.site.register(BookmarksUser, BookmarksUserAdmin)




