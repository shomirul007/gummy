import requests
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

class SentimentAnalysisAPIView(APIView):
    headers = {'User-agent': 'Mozilla/5.0'}
    keywords = ['Pets', 'DevOps']  # Add more keywords as needed

    def get_subreddit_posts(self, subreddit):
        """Fetch top posts (with more than 5 comments) from a subreddit."""
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=100"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            posts = response.json().get('data', {}).get('children', [])
            valid_posts = [post for post in posts if post['data'].get('num_comments', 0) >= 5]
            return valid_posts
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
            return [comment['data'].get('body', '') for comment in comments]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching comments for post {post_id} in subreddit {subreddit}: {e}")
            return []

    def analyze_sentiment(self, comments):
        """Analyze sentiment of given comments."""
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = {
            'hot': [],
            'pain_and_anger': [],
            'solution_requests': []
        }

        for comment in comments:
            score = analyzer.polarity_scores(comment)
            compound_score = score['compound']
            
            # Classify based on sentiment scores
            if compound_score >= 0.05:
                sentiment_scores['hot'].append(comment)
            elif compound_score <= -0.05:
                if "pain" in comment or "angry" in comment or "hate" in comment:  # Customize keywords as needed
                    sentiment_scores['pain_and_anger'].append(comment)
                else:
                    sentiment_scores['solution_requests'].append(comment)

        return sentiment_scores

    def get(self, request):
        results = {}
        
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
                        sentiment_results = self.analyze_sentiment(comments)

                        # Combine results
                        for category, comments_list in sentiment_results.items():
                            if category not in results:
                                results[category] = []
                            results[category].extend(comments_list)

        return Response(results, status=status.HTTP_200_OK)

    def get_subreddit_data(self, keyword):
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