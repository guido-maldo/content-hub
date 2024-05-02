# Create your views here.
from django.views.generic import ListView
from django.shortcuts import render
from .models import YouTubeVideo, RedditDiscussion, News, PodcastEpisode

def homepage(request):
    return render(request, 'homepage.html')
    
class VideosPageView(ListView):
    template_name = 'videos_page.html'
    model = YouTubeVideo
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = YouTubeVideo.objects.all()[:10]
        return context
    
class DicussionPageView(ListView):
    template_name = 'discussion_page.html'
    model = RedditDiscussion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reddit_posts'] = RedditDiscussion.objects.all()[:10]
        return context
    
class NewsPageView(ListView):
    template_name = 'news_page.html'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.filter().order_by('-pub_date')[:10]
        return context
    
class PodcastsPageView(ListView):
    template_name = 'podcasts_page.html'
    model = PodcastEpisode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episodes'] = PodcastEpisode.objects.filter().order_by('-pub_date')[:10]
        return context
