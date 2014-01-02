# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Tag
from ..bookmarks.views import BookmarksListView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TagAutocompleteView(ListView):
    model = Tag
    context_object_name = 'tags_list'

    def get_term(self):
        term = self.request.GET.get('term', None)
        return term

    def render_to_response(self, context, **response_kwargs):
        term = self.get_term()
        if term is None:
            return super(TagAutocompleteView, self).\
                render_to_response(context, **response_kwargs)
        queryset = self.model.objects.filter(
            name__istartswith=term)[:10]
        content = json.dumps([tag.name for tag in queryset])
        return HttpResponse(
            content,
            content_type='application/json',
            **response_kwargs
        )


class TagPageView(BookmarksListView):
    model = Tag
    context_object_name = 'bookmark_list'
    template_name = 'tags/tag_list.html'

    def get_tag_name(self):
        tag_name = self.kwargs.get('tag_name')
        return tag_name

    def get_queryset(self):
        tag = get_object_or_404(self.model, name=self.get_tag_name())
        bookmarks = tag.bookmarks.order_by('-id')
        return bookmarks

    def get_context_data(self, **kwargs):
        ctx = super(TagPageView, self).get_context_data(**kwargs)
        ctx['tag_name'] = self.get_tag_name()
        return ctx


class TagCloudView(ListView):
    model = Tag
    template_name = 'tags/tag_cloud.html'
    context_object_name = 'tag_list'
    MAX_WEIGHT = 22
    MIN_WEIGHT = 8

    def get_queryset(self):
        return super(TagCloudView, self).get_queryset(). \
            order_by('name')

    def get_context_data(self, **kwargs):
        ctx = super(TagCloudView, self).get_context_data(**kwargs)
        tags = self.get_queryset()
        # Calculate tag, min and max counts
        min_count = max_count = tags[0].bookmarks.count()
        for tag in tags:
            tag.count = tag.bookmarks.count()
            if tag.count < min_count:
                min_count = tag.count
            if max_count < tag.count:
                max_count = tag.count
        # Calculate count range. Avoid dividing by zero
        range = float(max_count - min_count)
        if range == 0.0:
            range = 1.0
        # Calculate tag weights
        for tag in tags:
            tag.weight = max(self.MIN_WEIGHT, int(self.MAX_WEIGHT * (tag.count - min_count) / range))
        ctx[self.context_object_name] = tags
        return ctx







