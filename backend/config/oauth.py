from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter OAuth Configuration
TWITTER_CLIENT_ID = os.getenv('TWITTER_CLIENT_ID')
TWITTER_CLIENT_SECRET = os.getenv('TWITTER_CLIENT_SECRET')
TWITTER_CALLBACK_URL = os.getenv('TWITTER_CALLBACK_URL', 'http://localhost:8000/auth/twitter')
TWITTER_AUTHORIZATION_ENDPOINT = 'https://twitter.com/i/oauth2/authorize'
TWITTER_ACCESS_TOKEN_ENDPOINT = 'https://api.twitter.com/2/oauth2/token'
TWITTER_API_BASE_URL = 'https://api.twitter.com/2/'

# Validate credentials
if not TWITTER_CLIENT_ID or not TWITTER_CLIENT_SECRET:
    raise ValueError("Twitter OAuth credentials are missing. Please check your .env file.")

oauth = OAuth()
oauth.register(
    name='twitter',
    client_id=TWITTER_CLIENT_ID,
    client_secret=TWITTER_CLIENT_SECRET,
    server_metadata_url='https://twitter.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'tweet.read users.read offline.access'
    }
)

def get_twitter_oauth_client():
    return oauth.create_client('twitter')

def get_twitter_credentials():
    return {
        'client_id': TWITTER_CLIENT_ID,
        'client_secret': TWITTER_CLIENT_SECRET,
        'callback_url': TWITTER_CALLBACK_URL
    }
