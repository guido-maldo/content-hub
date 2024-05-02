from django.contrib import admin

# Register your models here.
from .models import YouTubeVideo, RedditDiscussion, News, PodcastEpisode

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'title', 'upload_date')

@admin.register(RedditDiscussion)
class RedditDiscussionAdmin(admin.ModelAdmin):
    list_display = ('redditor', 'subreddit_name', 'title', 'post_date')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('source', 'title', 'pub_date')

@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('podcast_name', 'title', 'pub_date')
