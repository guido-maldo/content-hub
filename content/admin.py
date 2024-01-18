from django.contrib import admin

# Register your models here.
from .models import PodcastEpisode

@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('podcast_name', 'title', 'pub_date')
