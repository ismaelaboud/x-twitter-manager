import os
from typing import Dict, List
import tweepy
from dotenv import load_dotenv

load_dotenv()

class AccountManager:
    def __init__(self):
        self.accounts: Dict[str, tweepy.API] = {}

    def add_account(self, username: str, api_key: str, api_secret: str, 
                    access_token: str, access_token_secret: str):
        """
        Dynamically add a new Twitter account to management
        
        :param username: Unique identifier for the account
        :param api_key: Twitter API Key
        :param api_secret: Twitter API Secret
        :param access_token: Access Token
        :param access_token_secret: Access Token Secret
        """
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth)
        
        try:
            # Verify credentials
            api.verify_credentials()
            self.accounts[username] = api
            print(f"Account {username} added successfully!")
            return True
        except Exception as e:
            print(f"Failed to add account {username}: {e}")
            return False

    def remove_account(self, username: str):
        """
        Remove an account from management
        
        :param username: Username to remove
        """
        if username in self.accounts:
            del self.accounts[username]
            print(f"Account {username} removed successfully!")
        else:
            print(f"Account {username} not found!")

    def get_accounts(self) -> List[str]:
        """
        Get list of managed account usernames
        
        :return: List of usernames
        """
        return list(self.accounts.keys())

    def get_account(self, username: str):
        """
        Get specific account's API instance
        
        :param username: Username to retrieve
        :return: Tweepy API instance or None
        """
        return self.accounts.get(username)
