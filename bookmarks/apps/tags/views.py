# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Tag

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

