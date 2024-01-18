from django.contrib import admin

# Register your models here.
from .models import PodcastEpisode, YouTubeVideo

@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('podcast_name', 'title', 'pub_date')

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'title', 'upload_date')
