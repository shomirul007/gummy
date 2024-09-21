import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import Timeout

class SubredditAutocomplete(APIView):
    def get(self, request, keyword):
        url = f"https://www.reddit.com/api/subreddit_autocomplete.json?query={keyword}"
        headers = {'User-agent': 'Mozilla/5.0'}

        try:
            # Fetch subreddit autocomplete data from Reddit API
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Extract subreddits from the response
            subreddits = response.json().get('subreddits', [])
            
            # Calculate the total number of subreddits
            total_subreddits = len(subreddits)
            
            # Calculate the total number of subscribers (users)
            total_users = sum(subreddit.get('numSubscribers', 0) for subreddit in subreddits)
            
            # Format the response in the desired format
            result = [{
                "keyword": keyword,
                "subreddit": total_subreddits,
                "users": total_users
            }]
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Timeout:
            return Response({"error": "Request timed out. Please try again."}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubredditAbout(APIView):
    def get(self, request, subreddit_name):
        url = f"https://www.reddit.com/r/{subreddit_name}/about.json"
        headers = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return Response(response.json()['data'], status=status.HTTP_200_OK)
        return Response(response.json(), status=response.status_code)
