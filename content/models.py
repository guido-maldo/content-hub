from django.db import models

# Create your models here.

class YouTubeVideo(models.Model):
    video_id = models.CharField(max_length=50)
    thumbnail = models.URLField()
    title = models.CharField(max_length=200)
    channel_image = models.URLField()
    channel_name = models.CharField(max_length=100)
    duration = models.DurationField()
    upload_date = models.DateTimeField()
    category = models.CharField(max_length=100)
    view_count = models.CharField(max_length=50)
    like_count = models.CharField(max_length=50)
    player = models.TextField()

    def __str__(self) -> str:
        return f'{self.channel_name}: {self.title}'
    
class RedditDiscussion(models.Model):
    post_id = models.CharField(max_length=50)
    thumbnail = models.URLField()
    title = models.CharField(max_length=200)
    post_date = models.DateTimeField()
    media_type = models.CharField(max_length=10)
    redditor = models.CharField(max_length=50)
    subreddit_name = models.CharField(max_length=100)
    comments_count = models.PositiveIntegerField()
    score = models.IntegerField()
    content_url = models.URLField()
    hyperlink = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.redditor} | {self.subreddit_name}: {self.title}'
    
class News(models.Model):
    title = models.CharField(max_length=200, default='N/A')
    pub_date = models.DateTimeField(null=True)
    link = models.URLField(default='N/A')
    image = models.URLField(null=True, default='hyperlink_icon')
    source = models.CharField(max_length=100, default='N/A')
    source_homepage = models.URLField(default='N/A')
    guid = models.CharField(max_length=50, default='N/A')

    def __str__(self) -> str:
        return f'{self.source}: {self.title}'

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
    