from typing import Dict, List, Any
from datetime import datetime, timedelta
import pandas as pd
import tweepy

class AnalyticsService:
    def __init__(self, account_manager):
        self.account_manager = account_manager
        self.analytics_data: Dict[str, List[Dict[str, Any]]] = {}
    
    def collect_account_metrics(self, username: str):
        """
        Collect comprehensive metrics for a Twitter account
        
        :param username: Twitter account username
        :return: Dictionary of account metrics
        """
        api = self.account_manager.get_account(username)
        if not api:
            return None
        
        try:
            # Fetch user information
            user = api.get_user(screen_name=username)
            
            # Collect recent tweets
            recent_tweets = api.user_timeline(screen_name=username, count=200)
            
            # Analyze tweet metrics
            tweet_metrics = [{
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'retweet_count': tweet.retweet_count,
                'favorite_count': tweet.favorite_count
            } for tweet in recent_tweets]
            
            metrics = {
                'followers_count': user.followers_count,
                'friends_count': user.friends_count,
                'statuses_count': user.statuses_count,
                'total_engagement': sum(
                    tweet['retweet_count'] + tweet['favorite_count'] 
                    for tweet in tweet_metrics
                ),
                'average_engagement': (
                    sum(tweet['retweet_count'] + tweet['favorite_count'] 
                        for tweet in tweet_metrics) / len(tweet_metrics)
                    if tweet_metrics else 0
                ),
                'recent_tweets': tweet_metrics
            }
            
            # Store analytics data
            self.analytics_data[username] = tweet_metrics
            
            return metrics
        
        except Exception as e:
            print(f"Analytics collection error: {e}")
            return None
    
    def generate_engagement_report(self, username: str, days: int = 30):
        """
        Generate an engagement report for a specified period
        
        :param username: Twitter account username
        :param days: Number of days to analyze
        :return: Engagement report
        """
        if username not in self.analytics_data:
            self.collect_account_metrics(username)
        
        tweets = self.analytics_data.get(username, [])
        
        # Filter tweets within specified days
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_tweets = [
            tweet for tweet in tweets 
            if tweet['created_at'] >= cutoff_date
        ]
        
        # Create DataFrame for analysis
        df = pd.DataFrame(recent_tweets)
        
        report = {
            'total_tweets': len(recent_tweets),
            'total_retweets': df['retweet_count'].sum(),
            'total_likes': df['favorite_count'].sum(),
            'average_retweets': df['retweet_count'].mean(),
            'average_likes': df['favorite_count'].mean(),
            'top_performing_tweets': df.nlargest(3, 'retweet_count').to_dict('records')
        }
        
        return report
    
    def compare_accounts(self, usernames: List[str]):
        """
        Compare metrics across multiple accounts
        
        :param usernames: List of Twitter usernames
        :return: Comparative analytics
        """
        account_metrics = {}
        
        for username in usernames:
            metrics = self.collect_account_metrics(username)
            if metrics:
                account_metrics[username] = metrics
        
        return account_metrics
