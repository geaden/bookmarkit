# -*- coding: utf-8 -*-
import json
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404
from django.utils import timezone
from django.views.generic import ListView, FormView, DetailView
from rest_framework import permissions

from rest_framework.generics import GenericAPIView

from .models import Bookmark, Link, SharedBookmark
from .forms import BookmarkSaveForm
from ..tags.models import Tag

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


def get_favicon(url):
    """
    Returns link to favicon
    """
    return 'http://www.google.com/s2/favicons?domain_url={0}'.format(
        url)


class BookmarkAnswer(object):
    """
    Class to form answer after sharing result.
    """
    def __init__(self, bookmark, created=False):
        self.pk = bookmark.pk
        self.favicon = bookmark.favicon
        self.title = bookmark.title
        self.url = bookmark.link.url
        self.shared = bookmark.is_shared
        self.created = created
        self.tags = [tag.name for tag in bookmark.tag_set.all()]

    def to_json(self):
        return json.dumps(
            self.__dict__, ensure_ascii=True, indent=4)


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
            content = BookmarkAnswer(bookmark, created).to_json()
            return HttpResponse(content=content, content_type='application/json')
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


class BookmarkVoteAPIView(GenericAPIView):
    model = SharedBookmark
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            shared_bookmark = self.model.objects.get(id=request.POST.get('bookmark'))
            user_voted = shared_bookmark.user_voted.filter(email=request.user.email)
            if not user_voted:
                shared_bookmark.votes += 1
                shared_bookmark.user_voted.add(request.user)
                shared_bookmark.save()
                return HttpResponse(
                    content=json.dumps(
                        {'votes': shared_bookmark.votes,
                         'bookmark': BookmarkAnswer(
                             shared_bookmark.bookmark).__dict__},
                        indent=4),
                    content_type='application/json')
            else:
                return HttpResponseBadRequest()
        except ObjectDoesNotExist:
            raise Http404('Bookmark not found.')


class BookmarkShareAPIView(GenericAPIView):
    model = SharedBookmark

    def post(self, request, *args, **kwargs):
        bookmark_id = request.POST.get('bookmark')
        try:
            bookmark = Bookmark.objects.get(pk=bookmark_id)
            self.model.objects.create(
                bookmark=bookmark)
            answer = BookmarkAnswer(bookmark).to_json()
            return HttpResponse(
                content=answer,
                content_type='application/json')
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()
        except IntegrityError, e:
            shared_bookmark = self.model.objects.get(bookmark_id=bookmark_id)
            shared_bookmark.delete()
            bookmark = Bookmark.objects.get(pk=bookmark_id)
            answer = BookmarkAnswer(bookmark).to_json()
            return HttpResponse(
                content=answer, content_type='application/json')


class PopularListView(BookmarksListView):
    model = SharedBookmark
    template_name = 'bookmarks/popular_list.html'

    def get_queryset(self):
        shared_bookmarks = super(PopularListView, self).get_queryset()
        # today = timezone.now().today()
        # yesterday = today - datetime.timedelta(1)
        # shared_bookmarks = shared_bookmarks.filter(date__gt=yesterday)
        return shared_bookmarks.order_by('-votes')


class BookmarkPageView(DetailView):
    model = SharedBookmark
    template_name = 'bookmarks/bookmark_detail.html'
    context_object_name = 'shared_bookmark'

