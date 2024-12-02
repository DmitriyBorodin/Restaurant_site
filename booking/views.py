from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "booking/main.html"

class AboutView(TemplateView):
    template_name = "booking/about_us.html"