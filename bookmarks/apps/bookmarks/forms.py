# -*- coding: utf-8 -*-
from django import forms

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BookmarkSaveForm(forms.Form):
    url = forms.URLField(label='URL',
                         widget=forms.TextInput(attrs={'size': 64}))
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(attrs={'size': 64}))
    # tags = forms.CharField(label='Tags')