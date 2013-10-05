# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Folder

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class FolderSerializer(serializers.ModelSerializer):
    id = serializers.RelatedField()

    class Meta:
        model = Folder
        fields = (
            'id',
            'name',
            'icon'
        )

