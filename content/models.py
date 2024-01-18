from django.db import models

# Create your models here.

class PodcastEpisode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.CharField(max_length=100)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.podcast_name}: {self.title}'
    
class YouTubeVideo(models.Model):
    title = models.CharField(max_length=200)
    upload_date = models.DateTimeField()
    channel_name = models.CharField(max_length=100)
    channel_image = models.URLField()
    video = models.URLField()
    duration = models.CharField(max_length=50)
    view_count = models.CharField(max_length=50)
    like_ratio = models.CharField(max_length=50)
    video_id = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.channel_name}: {self.title}'
    