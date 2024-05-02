# Content Hub: A Content Aggregator Web Application
>Note: The project was built with Python 3.11

## Overview
**Content Hub** is a web application designed to keep users connected with the latest and trending digital content across multiple platforms into one user-friendly interface. By aggregating diverse popular media sources into a single, streamlined interface, Content Hub showcases current trends and popular media, enhancing user engagement and information discovery.

## Key Features

### YouTube Video Integration
- **Trending Videos**: Automatically fetches the top 10 trending YouTube videos.
- **Video Details**: Displays key information including title, YouTube channel, duration, upload date, video category, view count, and like count.
- **In-App Viewing**: Users can watch these videos directly within the app via embedded YouTube players, allowing for a seamless viewing experience without the need to navigate away from the page.

### Reddit Post Insights
- **Trending Posts**: Shows the top 10 trending posts from Reddit's r/all/hot, ensuring users are up-to-date with the most discussed topics across Reddit's vast community.
- **Post Details**: Displays key information including title, posted date, type of media, redditor, subreddit, comments count, and upvote count
- **In-App Viewing**: Users can view these posts directly within the app via embedded Iframes and dive into discussion by clicking on the embedded post to see its open discussion on Reddit.

### Yahoo News Headlines
- **Latest News**: Retrieves the top 10 headlines from Yahoo's latest news feed, ensuring users have access to breaking news and recent developments.
- **Article Details**: Displays key information including title, published date, and news source.
- **Direct Access**: Includes a link directly to the full article on Yahoo’s news portal for in-depth coverage and a link to the news source homepage.

### Podcast Episode Updates
- **Python Podcasts**: Features the latest 10 episodes from two prominent Python-focused podcast shows, making it a valuable resource for developers or tech enthusiasts interested in Python programming and related discussions.
- **Direct Access**: Includes a link directly to play podcast episodes to streamline their listening experience.

## Utility and User Experience
Content Hub leverages responsive design to ensure a smooth user experience in the browser. With its intuitive interface, users can easily navigate between different media categories and stay informed and entertained with minimal effort.

## Ideal For
This app is pefect for anyone looking to stay on top of the latest trends and discussions in technology, entertainment, and news across different platforms without the hassle of juggling multiple apps or browsing numerous websites.

---

# How to try out Content Hub

## Key Technologies and Libraries
- **Python**: Primary programming language used for backend development.
- **HTML**: Used for structuring the web app's content.
- **CSS**: Styles the web app's presentation.
- **JavaScript**: Enhances interactivity and user interface behaviors.
- **Bootstrap**: Framework for designing responsive and mobile-first websites.
- **Django**: High-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django APScheduler**: Integrates APScheduler with Django for running scheduled tasks.
- **Feedparser**: Parses RSS/Atom feeds in Python, used for retrieving news and podcast updates.
- **Requests**: Allows sending HTTP requests in Python, used for API interactions to fetch content from YouTube, Reddit, etc.
- **Praw**: The Python Reddit API Wrapper that makes it simple and straightforward to access Reddit data for trending posts.

## How to install
### Clone the git repository:
```$ git clone https://github.com/guido-maldo/content-hub.git```

This command will create a local copy of the repository in a folder named `content-hub` in your current working directory.

Navigate into the project directory
`$ cd content-hub`

### Generate a Django secret Key for your Django project using a Python script:
>This app requires three unique keys to function: a Django secret key, a YouTube Data API v3 key, and a Reddit API key
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

To generate a YouTube Data API v3 key, you'll need to use the Google Cloud Console to create a project and enable the YouTube Data API. Here’s a guide on how to do it:
1. Create or select a project:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - If you don’t have a Google Cloud project, you'll need to create one.
    - If you already have a project, select it from the project dropdown list at the top.
2. Enable the YouTube Data API:
    - In the navigation menu, go to "APIs & Services" > "Library".
    - Search for "YouTube Data API v3".
    - Click on it and then click "Enable" to enable the API for your selected project.
3. Create credentials:
    - After enabling the API, click on "Create Credentials" in the top bar.
    - Choose “YouTube Data API v3” from the list of APIs.
4. Get your API key:
    - Google will then generate an API key for you. This key is what you’ll use in your applications to interact with the YouTube Data API.

To generate a Reddit API key (commonly known as a client ID and client secret), you need to create a Reddit application in your Reddit account. Here’s a guide on how to do it:
1. Log in to Reddit:
    - Go to [Reddit](https://www.reddit.com/) and log in with your account.
2. Access the Developer Page:
    - Navigate to the [Reddit Apps page](https://www.reddit.com/prefs/apps). You can get there by clicking on your username, selecting 'Settings', then 'Safety & Privacy', and finally scrolling to the bottom and clicking on 'Manage third-party app authorization'.
3. Create a New Application:
    - At the bottom of the page, click on the "Create Another App" button.
    - Fill out the form with the following details:
        - Name: Give your application a name.
        - App type: Choose the type of your application. For most integrations, "script" is appropriate.
        - Description (optional): Provide a brief description of what your app will do.
        - About URL (optional): A URL with information about the app.
        - Redirect URI: For a script type application, you can use http://localhost:8000
4. Submit and Generate Credentials:
    - Click the "Create app" button at the bottom when you've filled out the form.
    - After the application is created, you will see a "Client ID" under the application name and a "Client Secret". The Client ID is public, and the Client Secret should be kept confidential.

### Create an `.env` file to hold all your secret keys:
>This is required because this project reads the secret keys from a .env file to work
1. Create the `.env` file from the root of the project directory
```$ touch .env```

2. Add Secret Keys
Open the `.env` file in a text editor and add your secret keys in the following format:
```
SECRET_KEY=your_django_secret_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
REDDIT_API_KEY=your_reddit_api_key_here
```

### Configure settings.py
Open the `setting.py` file in a text editor and replace `REDDIT_APP_CLIENT_ID` with your reddit application client id
```REDDIT_APP_CLIENT_ID = 'your_reddit_app_client_id_here'```

### Create and activate a Python virtual environment for your operating system
```
$ python -m venv .venv
$ .\venv\Scripts\activate
```

### Install the dependencies from  the `requirements.txt` or `poetry.lock` file:
- using the python `pip` package manager
```(.venv) $ python -m pip install -r <path_to_requirements.txt>```

- using `poetry`
```(.venv) $ poetry install```

### Start the Django development server:
```
(.venv) $ cd content-hub
(.venv) $ python manage.py runserver localhost:8000
```
You can now navigate to `localhost:8000` in your browser and inspect the finished project.