from django.shortcuts import render
from django.views.generic import View, TemplateView
# Create your views here.


class HomePageView(TemplateView):

    template_name = 'home/homepage.html'