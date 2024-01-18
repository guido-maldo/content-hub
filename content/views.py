from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import PodcastEpisode

class HomePageView(ListView):
    template_name = "homepage.html"
    model = PodcastEpisode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = PodcastEpisode.objects.filter().order_by("-pub_date")[:10]
        return context