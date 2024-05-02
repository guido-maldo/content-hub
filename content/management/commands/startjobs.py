# Standard Library
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
import praw
import feedparser
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from dateutil import parser
from isodate import parse_duration
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from content.models import YouTubeVideo, RedditDiscussion, News, PodcastEpisode

_logger = logging.getLogger(__name__)

def save_new_videos(videos):
    """Saves new YouTube videos to the database.

    Updates the database with the new list of `YouTubeVideo`s that are trending by
    replacing each stored video through its id.

    Args:
        videos: requires a list of video resources that represent YouTube videos.
    """
    channels_url: str = 'https://www.googleapis.com/youtube/v3/channels'
    video_categories_url: str = 'https://www.googleapis.com/youtube/v3/videoCategories'
    api_key: str = settings.YOUTUBE_API_KEY

    for index, video in enumerate(videos, start=1):
        payload = {
            'key': api_key,
            'part': 'snippet',
            'id': f'{video["snippet"]["channelId"]}',
        }
        response = _get(channels_url, payload)
        channel = response.get('items')[0]

        payload = {
            'key': api_key,
            'part': 'snippet',
            'id': f'{video["snippet"]["categoryId"]}',
        }
        response = _get(video_categories_url, payload)
        video_category = response.get('items')[0]

        # get() is used to avoid values that cannot be possibly found which are `None` and cannot be stored in the database
        youtube_video = YouTubeVideo(
            id = index,
            title = video['snippet']['title'],
            upload_date = parser.parse(video['snippet']['publishedAt']),
            channel_name = video['snippet']['channelTitle'],
            channel_image = channel['snippet']['thumbnails']['medium']['url'],
            thumbnail = video['snippet']['thumbnails']['medium']['url'],
            player = video['player']['embedHtml'],
            category = video_category.get('snippet').get('title', 'n/a'),
            duration = parse_duration(video['contentDetails']['duration']),
            view_count = video.get('statistics').get('viewCount', 'n/a'),
            like_count = video.get('statistics').get('likeCount', 'n/a'),
            video_id = video['id'],    
        )
        youtube_video.save()

def save_new_posts(posts):
    """Saves new Reddit posts to the database.

    Updates the database with the new list of `RedditDiscussion`s that are trending by
    replacing each stored post through its id.

    Args:
        posts: requires a list of resources that represent Reddit posts.
    """
    for index, submission in enumerate(posts, start=1):
            media_type = _get_reddit_submission_type(submission)
            thumbnail = _get_reddit_post_thumbnail(submission, media_type)

            reddit_content = RedditDiscussion(
                id = index,
                post_id = submission.id,
                thumbnail = thumbnail, 
                title = submission.title,
                post_date = datetime.fromtimestamp(submission.created),
                media_type = media_type,
                redditor = 'u/' + submission.author.name,
                subreddit_name = submission.subreddit_name_prefixed,
                comments_count = submission.num_comments,
                score = submission.score,
                content_url = submission.permalink,
                hyperlink = submission.url,
            )
            reddit_content.save()

def save_new_news(feed):
    """Saves new news to the database.

    Checks the news GUID against the news currently stored in the
    database. If not found, then a new `News` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    for item in feed.entries:
        if not News.objects.filter(guid=item.guid).exists():
            news = News(
                title=item.title,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=item.media_content[0]['url'],
                source=item.source.title,
                source_homepage=item.source.href,
                guid = item.guid,
            )
            news.save()

def save_new_episodes(feed):
    """Saves new podcast episodes to the database.

    Checks the episode GUID against the episodes currently stored in the
    database. If not found, then a new `PodcastEpisode` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image['href']

    for item in feed.entries:
        if not PodcastEpisode.objects.filter(guid=item.guid).exists():
            episode = PodcastEpisode(
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()

def _get(url, payload):
    """Returns a request response object in json format for a url with any number of parameters."""
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
    except HTTPError as e:
        print(f'Error response status code : {e.status_code}, reason : {e.error_details}')
    else:
        return response.json()
    
def _get_reddit_submission_type(post):
    if 'gif' in post.url:
        return 'GIF'
    elif post.is_reddit_media_domain:
        if post.is_video:
            return 'Video'
        return 'Image'
    elif vars(post).get('is_gallery', False):
        return 'Gallery'
    elif post.is_self:
        return 'Text'
    else:
        return 'Hyperlink'
    
def _get_reddit_post_thumbnail(post, media_type):
    thumbnail_url = post.thumbnail

    if thumbnail_url.startswith('http'):
        return thumbnail_url
    elif vars(post).get('preview', False):
        return post.preview['images'][0]['source']['url']
    elif media_type == 'Video' or media_type == 'GIF':
        return str(settings.STATICFILES_DIRS[0]) + '\imgs\\video_play_icon.svg'
    elif media_type == 'Image':
        return str(settings.STATICFILES_DIRS[0]) + '\imgs\image_icon.svg'
    elif media_type == 'Gallery':
        return str(settings.STATICFILES_DIRS[0]) + '\imgs\gallery_icon.svg'
    elif media_type == 'Text':
        return str(settings.STATICFILES_DIRS[0]) + '\imgs\\text_icon.svg'
    else:
        return str(settings.STATICFILES_DIRS[0]) + '\imgs\hyperlink_chain_icon.png'

def fetch_youtube_videos():
    """Fetches new videos from YouTube Data API for YouTube Trending Now"""
    videos_trending_url: str = 'https://www.googleapis.com/youtube/v3/videos'

    payload = {
        'key': settings.YOUTUBE_API_KEY,
        'chart': 'mostPopular',
        'part': 'snippet,contentDetails,statistics,player',
        'regionCode': 'US',
    }

    response = _get(videos_trending_url, payload)
    _videos = response.get('items')
    _logger.debug('Got %d videos from YouTube', len(_videos))

    cursor = response.get('nextPageToken')
    while cursor:
        payload['pageToken'] = cursor
        response = _get(videos_trending_url, payload)
        cursor = response.get('nextPageToken')
        _videos.extend(response.get('items'))
    _logger.debug('Got %d videos from YouTube', len(_videos))    

    save_new_videos(_videos)

def fetch_reddit_posts():
    """Fetches new popular posts from the Reddit's 'All' subreddit
    using the PRAW package for simple access to Reddit's API"""
    
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=settings.REDDIT_APP_CLIENT_ID,
                         client_secret=settings.REDDIT_API_KEY,
                         user_agent='chrome:content_hub:v0.1 (by u/gjmaldon)')
    
    # Fetch popular posts from the 'All' subreddit
    subreddit = reddit.subreddit('all')
    _popular_posts = subreddit.hot()
    _logger.debug('Got posts from Reddit') 

    save_new_posts(_popular_posts)

def fetch_news():
    """Fetches new news from RSS for Yahoo News - Latest News & Headlines"""
    _feed = feedparser.parse('https://yahoo.com/news/rss')
    save_new_news(_feed) 

def fetch_realpython_episodes():
    """Fetches new episodes from RSS for The Real Python Podcast."""
    _feed = feedparser.parse('https://realpython.com/podcasts/rpp/feed')
    save_new_episodes(_feed)

def fetch_talkpython_episodes():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse('https://talkpython.fm/episodes/rss')
    save_new_episodes(_feed)

def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)    

def run_all_fetch_jobs():
    fetch_youtube_videos()
    fetch_reddit_posts()
    fetch_news()
    fetch_realpython_episodes()
    fetch_talkpython_episodes()

class Command(BaseCommand):
    help = 'Runs apscheduler.'

    def handle(self, *args, **options):
        run_all_fetch_jobs()

        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            fetch_youtube_videos,
            trigger='interval',
            minutes=60,
            id='YouTube Trending Now Feed',
            max_instances=1,
            replace_existing=True,
        )
        _logger.info('Added job: YouTube Trending Now Feed.')

        scheduler.add_job(
            fetch_reddit_posts,
            trigger='interval',
            minutes=60,
            id='Reddit Popular Posts Feed',
            max_instances=1,
            replace_existing=True,
        )
        _logger.info('Added job: Reddit Popular Posts Feed.')
        
        scheduler.add_job(
            fetch_news,
            trigger='interval',
            minutes=60,
            id='News Feed',
            max_instances=1,
            replace_existing=True,
        )
        _logger.info('Added job: Reddit Popular Posts Feed.')

        scheduler.add_job(
            fetch_realpython_episodes,
            trigger='interval',
            minutes=60,
            id='The Real Python Podcast',
            max_instances=1,
            replace_existing=True,
        )
        _logger.info('Added job: The Real Python Podcast.')

        scheduler.add_job(
            fetch_talkpython_episodes,
            trigger='interval',
            minutes=60,
            id='Talk Python Feed',
            max_instances=1,
            replace_existing=True,
        )
        _logger.info('Added job: Talk Python Feed.')

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),  # Midnight on Monday, before start of the next work week.
            id='Delete Old Job Executions',
            max_instances=1,
            replace_existing=True,
        )
        _logger.info('Added weekly job: Delete Old Job Executions.')

        try:
            _logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            _logger.info('Stopping scheduler...')
            scheduler.shutdown(wait=False)
            _logger.info('Scheduler shut down successfully!')