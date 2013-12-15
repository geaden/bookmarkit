# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView

from .models import Bookmark, Link
from .forms import BookmarkSaveForm

from ..tags.models import Tag

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BookmarksListView(ListView):
    model = Bookmark
    context_object_name = 'bookmark_list'
    paginate_by = 10


class BookmarkCreateEditView(FormView):
    model = Bookmark
    form_class = BookmarkSaveForm
    template_name = 'bookmarks/bookmark_form.html'
    success_url = reverse_lazy('bookmarks:main')

    def get_initial(self):
        initial = super(BookmarkCreateEditView, self).get_initial()
        if 'url' in self.request.GET:
            url = self.request.GET['url']
            title = ''
            tags = ''
            try:
                link = Link.objects.get(url=url)
                bookmark = Bookmark.objects.get(link=link,
                                                user=self.request.user)
                title = bookmark.title
                tags = ','.join(tag.name for tag in bookmark.tag_set.all())
            except ObjectDoesNotExist:
                pass
            initial.update({
                'url': url,
                'title': title,
                'tags': tags
            })
        return initial

    def form_valid(self, form):
        # Create or get link
        link, _ = Link.objects.get_or_create(
            url=form.cleaned_data['url'])
        # Create or get bookmark
        bookmark, created = Bookmark.objects.get_or_create(
            user=self.request.user, link=link)
        # Set bookmark tags
        # If the bookmark is being updated, clear old tag list.
        if not created:
            bookmark.tag_set.clear()
        # Create a new tag list
        tag_names = form.cleaned_data['tags'].split(',')
        for tag_name in tag_names:
            tag, dummy = Tag.objects.get_or_create(name=tag_name)
            bookmark.tag_set.add(tag)
        # Set bookmark title
        bookmark.title = form.cleaned_data['title']
        bookmark.save()
        return HttpResponseRedirect(self.get_success_url())
