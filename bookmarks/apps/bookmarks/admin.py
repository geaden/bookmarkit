# -*- coding: utf-8 -*-

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


from .models import Bookmark, Link, SharedBookmark
from django.contrib import admin


class BookmarkAdmin(admin.ModelAdmin):
    fields = ['title', 'link', 'user']
    list_display = ('title', 'link', 'user')
    list_filter = ('user', )
    ordering = ('title', )
    search_fields = ('title', )

admin.site.register(Bookmark, BookmarkAdmin)

admin.site.register(Link)
admin.site.register(SharedBookmark)

