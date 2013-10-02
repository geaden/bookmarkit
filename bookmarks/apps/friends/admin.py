# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Friendship, Invitation

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class FriendshipAdmin(admin.ModelAdmin):
    list_filter = ('from_friend', )

admin.site.register(Friendship, FriendshipAdmin)


class InvitationAdmin(admin.ModelAdmin):
    ordering = ('email', )

admin.site.register(Invitation, InvitationAdmin)