# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class AppView(TemplateView):
    template_name = 'app.html'