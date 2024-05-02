from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from .models import YouTubeVideo, RedditDiscussion, News, PodcastEpisode
from django.urls.base import reverse

class ContentTests(TestCase):
    def setUp(self):
        self.video = YouTubeVideo.objects.create(
            title = 'My Awesome YouTube Video',
            upload_date = timezone.now(),
            channel_name = 'The Creator',
            channel_image = 'https://channelimage.thecreator.com',
            thumbnail = 'https://thumbnail.thecreator.com',
            player = '<iframe src="//www.youtube.com/embed/ge19720" frameborder="0" allow="autoplay;" allowfullscreen></iframe>',
            category = 'Gaming',
            duration = timezone.timedelta(minutes=5, seconds=35),
            view_count = '100000',
            like_count = '1000',
            video_id = 'ge19720'
        )

        self.post = RedditDiscussion.objects.create(
            post_id = 're19723',
            thumbnail = 'https://thumbnail.thecreator.com',
            title = 'My Awesome Reddit Post',
            post_date = timezone.now(),
            media_type = 'Image',
            redditor = 'u/the_creator',
            subreddit_name = 'r/my_subreddit',
            comments_count = 123,
            score = 245,
            content_url = 'https://content.url.com',
            hyperlink = 'redd.it.post/my_awesome_reddit_post'
        )

        self.news = News.objects.create(
            title = 'My Awesome News Article',
            pub_date = timezone.now(),
            link = 'https://myawesomenewsarticle.com',
            image = 'https://image.myawesomenewsarticle.com',
            source = 'My Awesome News Source',
            source_homepage = 'https://awesomenewssource.com',
            guid = 'my-awesome-news-article-232031104.html',
        )
        
        self.episode = PodcastEpisode.objects.create(
            title = 'My Awesome Podcast Episode',
            description = 'Python is Cool!',
            pub_date = timezone.now(),
            link = 'https://myawesomeshow.com',
            image = 'https://image.myawesomeshow.com',
            podcast_name = 'My Python Podcast',
            guid = 'de194720-7b4c-49e2-a05f-432436d3fetr',
        )

    def test_video_content(self):
        self.assertEqual(self.video.title, 'My Awesome YouTube Video')
        self.assertEqual(self.video.channel_name, 'The Creator')
        self.assertEqual(self.video.player, '<iframe src="//www.youtube.com/embed/ge19720" frameborder="0" allow="autoplay;" allowfullscreen></iframe>')
        self.assertEqual(
            self.video.video_id, 'ge19720'
        )

    def test_video_str_representation(self):
        self.assertEqual(
            str(self.video), 'The Creator: My Awesome YouTube Video'
        ) 
        
    def test_post_content(self):
        self.assertEqual(self.post.title, 'My Awesome Reddit Post')
        self.assertEqual(self.post.subreddit_name, 'r/my_subreddit')
        self.assertEqual(self.post.content_url, 'https://content.url.com')
        self.assertEqual(
            self.post.post_id, 're19723'
        )

    def test_post_str_representation(self):
        self.assertEqual(
            str(self.post), 'u/the_creator | r/my_subreddit: My Awesome Reddit Post'
        ) 

    def test_news_content(self):
        self.assertEqual(self.news.title, 'My Awesome News Article')
        self.assertEqual(self.news.link, 'https://myawesomenewsarticle.com')
        self.assertEqual(
            self.news.guid, 'my-awesome-news-article-232031104.html'
        )

    def test_news_str_representation(self):
        self.assertEqual(
            str(self.news), 'My Awesome News Source: My Awesome News Article'
        )
        
    def test_episode_content(self):
        self.assertEqual(self.episode.description, 'Python is Cool!')
        self.assertEqual(self.episode.link, 'https://myawesomeshow.com')
        self.assertEqual(
            self.episode.guid, 'de194720-7b4c-49e2-a05f-432436d3fetr'
        )

    def test_episode_str_representation(self):
        self.assertEqual(
            str(self.episode), 'My Python Podcast: My Awesome Podcast Episode'
        )

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_video_page_status_code(self):
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, 200)        

    def test_discussion_page_status_code(self):
        response = self.client.get('/discussion/')
        self.assertEqual(response.status_code, 200)        
    
    def test_news_page_status_code(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)        
    
    def test_podcasts_page_status_code(self):
        response = self.client.get('/podcasts/')
        self.assertEqual(response.status_code, 200)        

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage.html')

    def test_video_page_uses_correct_template(self):
        response = self.client.get(reverse('videos_page'))
        self.assertTemplateUsed(response, 'videos_page.html')
    
    def test_discussion_page_uses_correct_template(self):
        response = self.client.get(reverse('discussion_page'))
        self.assertTemplateUsed(response, 'discussion_page.html')
    
    def test_news_page_uses_correct_template(self):
        response = self.client.get(reverse('news_page'))
        self.assertTemplateUsed(response, 'news_page.html')
    
    def test_podcasts_page_uses_correct_template(self):
        response = self.client.get(reverse('podcasts_page'))
        self.assertTemplateUsed(response, 'podcasts_page.html')

    def test_homepage_list_contents(self):
        response = self.client.get(reverse('homepage'))
        self.assertContains(response, 'Welcome to Content Hub!')

    def test_video_page_list_contents(self):
        response = self.client.get(reverse('videos_page'))
        self.assertContains(response, 'YouTube Trending Now')
    
    def test_discussion_page_list_contents(self):
        response = self.client.get(reverse('discussion_page'))
        self.assertContains(response, 'Reddit Trending Now')
    
    def test_news_page_list_contents(self):
        response = self.client.get(reverse('news_page'))
        self.assertContains(response, 'Latest News & Headlines')
    
    def test_podcasts_page_list_contents(self):
        response = self.client.get(reverse('podcasts_page'))
        self.assertContains(response, 'Python Podcasts')