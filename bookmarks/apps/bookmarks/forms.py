# -*- coding: utf-8 -*-
from django import forms

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


# TODO: get rid of repeat decoration
decoration = lambda x, s: {'class': 'form-control',
                           'placeholder': x,
                           'size': s}


class TagsWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('jquery.tagsinput.css',)
        }
        js = ('jquery.tagsinput.min.js', 'tags.js')


class BookmarkSaveForm(forms.Form):
    url = forms.URLField(widget=forms.TextInput(
        attrs=decoration(u'Url', 64)))
    title = forms.CharField(
        widget=forms.TextInput(attrs=decoration(u'Title', 64)))
    tags = forms.CharField(widget=forms.TextInput(
        attrs=decoration(u'Tags', 64)))