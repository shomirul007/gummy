import requests
import time
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse



logger = logging.getLogger(__name__)

class PostsAPIView(APIView):
    keywords = ['Pets']

    headers = {'User-agent': 'Mozilla/5.0'}

    def get_subreddit_posts(self, subreddit):
        """Fetch top posts (with more than 5 comments) from a subreddit."""
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=100"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            posts = response.json().get('data', {}).get('children', [])
            valid_posts = [post for post in posts if post['data'].get('num_comments', 0) >= 5]
            return valid_posts  # return valid_posts instead of posts
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching posts from subreddit {subreddit}: {e}")
            return []

    def get_post_comments(self, subreddit, post_id):
        """Fetch comments for a specific post."""
        url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            comments = response.json()[1].get('data', {}).get('children', [])
            return comments
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching comments for post {post_id} in subreddit {subreddit}: {e}")
            return []

    def get(self, request):
        results = []
        for keyword in self.keywords:
            subreddit_data = self.get_subreddit_data(keyword)
            subreddits = subreddit_data.get('subreddits', [])
            for subreddit in subreddits:
                subreddit_name = subreddit.get('name', '')
                if subreddit_name:
                    posts = self.get_subreddit_posts(subreddit_name)
                    for post in posts:
                        post_id = post['data']['id']
                        comments = self.get_post_comments(subreddit_name, post_id)
                        post_data = {
                            'subreddit': subreddit_name,
                            'post_title': post['data'].get('title', ''),
                            'post_url': post['data'].get('url', ''),
                            'num_comments': post['data'].get('num_comments', 0),
                            'comments': [comment['data'].get('body', '') for comment in comments]
                        }
                        results.append(post_data)
        return Response(results, status=status.HTTP_200_OK)

    def get_subreddit_data(self, keyword):
        time.sleep(1)
        """Fetch subreddits related to a keyword."""
        url = f"https://www.reddit.com/api/subreddit_autocomplete.json?query={keyword}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            subreddits = response.json().get('subreddits', [])
            return {'keyword': keyword, 'subreddits': subreddits}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching subreddits for keyword {keyword}: {e}")
            return {'keyword': keyword, 'subreddits': []}