from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from config.oauth import get_twitter_oauth_client
from starlette.config import Config
import tweepy

router = APIRouter()
config = Config('.env')

@router.get('/login/twitter')
async def twitter_login(request: Request):
    twitter_client = get_twitter_oauth_client()
    redirect_uri = request.url_for('twitter_auth')
    return await twitter_client.authorize_redirect(request, redirect_uri)

@router.get('/auth/twitter')
async def twitter_auth(request: Request):
    twitter_client = get_twitter_oauth_client()
    
    try:
        # Fetch access token
        token = await twitter_client.authorize_access_token(request)
        
        # Extract Twitter credentials
        oauth_token = token.get('oauth_token')
        oauth_token_secret = token.get('oauth_token_secret')
        
        # Authenticate with Tweepy
        auth = tweepy.OAuthHandler(
            config('TWITTER_CLIENT_ID'), 
            config('TWITTER_CLIENT_SECRET')
        )
        auth.set_access_token(oauth_token, oauth_token_secret)
        
        # Create API client
        api = tweepy.API(auth)
        
        # Fetch user details
        user = api.verify_credentials()
        
        # TODO: Save user details to database
        return {
            'user_id': user.id_str,
            'screen_name': user.screen_name,
            'profile_image_url': user.profile_image_url_https
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Twitter OAuth failed: {str(e)}')

@router.get('/logout/twitter')
async def twitter_logout(request: Request):
    # TODO: Implement logout logic
    # Clear session, revoke tokens, etc.
    return {'message': 'Logged out successfully'}
