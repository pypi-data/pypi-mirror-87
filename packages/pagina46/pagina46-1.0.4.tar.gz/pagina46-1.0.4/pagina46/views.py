from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View, TemplateResponseMixin, TemplateView


class Index(TemplateView):
    template_name = 'pagina46/base.html'
