from django.urls import path
from .views import homepage, VideosPageView, DicussionPageView, NewsPageView, PodcastsPageView

urlpatterns = [
    path('', homepage, name='homepage'),
    path('videos/', VideosPageView.as_view(), name='videos_page'),
    path('discussion/', DicussionPageView.as_view(), name='discussion_page'),
    path('news/', NewsPageView.as_view(), name='news_page'),
    path('podcasts/', PodcastsPageView.as_view(), name='podcasts_page'),
]