from typing import Optional, List
import tweepy
from backend.core.account_manager import AccountManager

class TweetHandler:
    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager

    def post_tweet(self, username: str, content: str, 
                   media_paths: Optional[List[str]] = None):
        """
        Post a tweet for a specific account
        
        :param username: Account to post from
        :param content: Tweet text
        :param media_paths: Optional list of media file paths
        """
        api = self.account_manager.get_account(username)
        
        if not api:
            print(f"Account {username} not found!")
            return False
        
        try:
            if media_paths:
                media_ids = [api.media_upload(media).media_id_string 
                             for media in media_paths]
                tweet = api.update_status(status=content, media_ids=media_ids)
            else:
                tweet = api.update_status(status=content)
            
            print(f"Tweet posted successfully for {username}")
            return tweet
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return False

    def create_thread(self, username: str, thread_tweets: List[str]):
        """
        Create a tweet thread
        
        :param username: Account to post thread from
        :param thread_tweets: List of tweet contents in order
        """
        api = self.account_manager.get_account(username)
        
        if not api:
            print(f"Account {username} not found!")
            return False
        
        try:
            previous_tweet = None
            for tweet_content in thread_tweets:
                if previous_tweet:
                    tweet = api.update_status(
                        status=tweet_content, 
                        in_reply_to_status_id=previous_tweet.id
                    )
                else:
                    tweet = api.update_status(status=tweet_content)
                
                previous_tweet = tweet
            
            print(f"Thread created successfully for {username}")
            return True
        except Exception as e:
            print(f"Error creating thread: {e}")
            return False

    def reply_to_tweet(self, username: str, tweet_id: str, reply_text: str):
        """
        Reply to a specific tweet
        
        :param username: Account replying from
        :param tweet_id: ID of tweet to reply to
        :param reply_text: Reply content
        """
        api = self.account_manager.get_account(username)
        
        if not api:
            print(f"Account {username} not found!")
            return False
        
        try:
            reply = api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet_id
            )
            print(f"Replied successfully from {username}")
            return reply
        except Exception as e:
            print(f"Error replying to tweet: {e}")
            return False
