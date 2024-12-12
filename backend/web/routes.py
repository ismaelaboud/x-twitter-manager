from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from backend.services.auth_service import AuthService
from backend.core.account_manager import AccountManager
from backend.core.tweet_handler import TweetHandler
import tweepy

app = FastAPI(title="X-Twitter Bot Dashboard")

# Initialize services
auth_service = AuthService()
account_manager = AccountManager()
tweet_handler = TweetHandler(account_manager)

class TwitterCredentials(BaseModel):
    username: str
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str

@app.post("/accounts/add")
async def add_twitter_account(credentials: TwitterCredentials):
    """
    Add a new Twitter account with API credentials
    """
    try:
        # Validate Twitter credentials
        auth = tweepy.OAuthHandler(credentials.api_key, credentials.api_secret)
        auth.set_access_token(credentials.access_token, credentials.access_token_secret)
        api = tweepy.API(auth)
        
        # Verify credentials
        api.verify_credentials()
        
        # Store encrypted credentials
        auth_service.add_account_credentials(
            credentials.username, 
            credentials.dict()
        )
        
        # Add to account manager
        account_manager.add_account(
            credentials.username, 
            credentials.api_key, 
            credentials.api_secret, 
            credentials.access_token, 
            credentials.access_token_secret
        )
        
        return {"status": "success", "message": f"Account {credentials.username} added"}
    
    except tweepy.TweepError as e:
        raise HTTPException(status_code=400, detail=f"Twitter API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/accounts/list")
async def list_twitter_accounts():
    """
    List all stored Twitter accounts
    """
    return {
        "accounts": auth_service.list_accounts()
    }

@app.delete("/accounts/remove/{username}")
async def remove_twitter_account(username: str):
    """
    Remove a Twitter account
    """
    try:
        auth_service.remove_account_credentials(username)
        account_manager.remove_account(username)
        return {"status": "success", "message": f"Account {username} removed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing account: {str(e)}")

@app.post("/tweets/post")
async def post_tweet(username: str, content: str):
    """
    Post a tweet for a specific account
    """
    result = tweet_handler.post_tweet(username, content)
    if result:
        return {"status": "success", "tweet_id": result.id}
    else:
        raise HTTPException(status_code=400, detail="Failed to post tweet")
