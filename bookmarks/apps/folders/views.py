# -*- coding: utf-8 -*-
from django.views.generic import ListView, UpdateView,\
    DeleteView, DetailView, CreateView

from .models import Folder, FolderSystem

from ..bookmarks.models import Bookmark

from .serializers import FolderSerializer

from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class FolderCreateView(CreateView):
    model = Folder


class FolderUpdateView(UpdateView):
    model = Folder


class FolderDetailView(DetailView):
    model = Folder

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        ctx = super(FolderDetailView, self).get_context_data(**kwargs)
        ctx['bookmarks'] = obj.bookmark_set.all()
        ctx['subfolders'] = obj.children.all()


class FolderListCreateView(ListCreateAPIView):
    model = Folder
    serializer_class = FolderSerializer


class FolderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    model = Folder
    serializer_class = FolderSerializer
