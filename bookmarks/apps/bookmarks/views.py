# -*- coding: utf-8 -*-
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.views.generic import ListView, FormView

from .models import Bookmark, Link
from .forms import BookmarkSaveForm

from ..tags.models import Tag

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


def get_favicon(url):
    """
    Returns link to favicon
    """
    return 'http://www.google.com/s2/favicons?domain_url={0}'.format(
        url)


class BookmarksListView(ListView):
    model = Bookmark
    context_object_name = 'bookmark_list'
    paginate_by = 20
    form_class = BookmarkSaveForm

    def get_queryset(self):
        # Put the last added bookmarks on top
        queryset = super(BookmarksListView, self).get_queryset()
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        ctx = super(BookmarksListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form_class()
        return ctx


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
        else:
            # Set favicon
            bookmark.favicon = get_favicon(link.url)
        # Create a new tag list
        tag_names = form.cleaned_data['tags'].split(',')
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            bookmark.tag_set.add(tag)
        # Set bookmark title
        bookmark.title = form.cleaned_data['title']
        bookmark.save()
        if 'ajax' in self.request.GET:
            content = {'url': bookmark.link.url,
                       'favicon': bookmark.favicon,
                       'title': bookmark.title,
                       'tags': [tag.name for tag in bookmark.tag_set.all()],
                       'created': created}
            return HttpResponse(content=json.dumps(content), content_type='application/json')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        if 'ajax' in self.request.GET:
            return HttpResponseBadRequest(content=json.dumps(form.errors),
                                          content_type='application/json')
        return super(BookmarkCreateEditView, self).form_invalid(form)


class BookmarkSearchView(BookmarksListView):
    def get_search_query(self):
        if 'query' in self.request.GET:
            query = self.request.GET.get('query').strip()
            if query:
                return query
        return None

    def get_queryset(self):
        query = self.get_search_query()
        if query is None:
            return super(BookmarkSearchView, self).get_queryset()
        keywords = query.split()
        q = Q()
        for keyword in keywords:
            q = q & Q(title__icontains=keyword)
        return self.model.objects.filter(q).order_by('-id')

    def get_context_data(self, **kwargs):
        ctx = super(BookmarkSearchView, self).get_context_data(**kwargs)
        query = self.get_search_query()
        if query is not None:
            ctx['show_results'] = True
            ctx['query'] = query
        return ctx