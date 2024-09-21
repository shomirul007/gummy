import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CuratedAPIView(APIView):
    keywords = ['Pet Lovers', 'Software Developers', 'DevOps', 'Crypto', 'Marketers']
    
    def get_subreddit_data(self, keyword):
        url = f"https://www.reddit.com/api/subreddit_autocomplete.json?query={keyword}"
        headers = {'User-agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            subreddits = response.json().get('subreddits', [])
            
            total_subs = len(subreddits)
            total_users = sum([subreddit.get('numSubscribers', 0) for subreddit in subreddits])
            
            return {
                'keyword': keyword,
                'subs': total_subs,
                'users': total_users
            }
        
        except requests.exceptions.RequestException:
            return {
                'keyword': keyword,
                'subs': 0,
                'users': 0
            }

    def get(self, request):
        results = [self.get_subreddit_data(keyword) for keyword in self.keywords]
        return Response(results, status=status.HTTP_200_OK)
