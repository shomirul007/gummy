import requests
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)
class CuratedAPIView(APIView):
    keywords = ['Pets', 'Software Developers', 'DevOps', 'Cryptocurrency', 'Marketers',
                'Startup Founders','Stock Investors','Video Editors', 'Generative AI', 'Designers', 
                'Data Scientists', 'Fitness Enthusiasts', 'Gardners', 'Photographers', 'NFT Collectors', 
                'Ecommerce', 'SEOs', 'Self-Promoters', 'Parents', 'No-code', 
                'Cloud Email', 'English Learners', 'Financial Independence', '3D Printers', 'Freelancers', 
                'Copywriters', 'Notion Users', 'Influencers', 'AirBnB Hosts', 'Advertisers', 
                'Remote Workers', 'Productivity', 'Product Managers', 'SaaS founders', 'B2B Sales', 
                'Restaurant Owners', 'Nwesletter Creators']
    
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
