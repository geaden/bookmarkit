# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView

from .models import Bookmark, Link
from .forms import BookmarkSaveForm

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BookmarksListView(ListView):
    model = Bookmark
    context_object_name = 'bookmark_list'


class BookmarkCreateView(FormView):
    model = Bookmark
    form_class = BookmarkSaveForm
    template_name = 'bookmarks/bookmark_form.html'
    success_url = reverse_lazy('bookmarks:main')

    def form_valid(self, form):
        #Create or get link
        link, _ = Link.objects.get_or_create(
            url=form.cleaned_data['url'])
        #Create or get bookmark
        bookmark, created = Bookmark.objects.get_or_create(
            user=self.request.user, link=link)
        #Update bookmark title
        bookmark.title = form.cleaned_data['title']
        bookmark.save()
        return HttpResponseRedirect(self.get_success_url())
