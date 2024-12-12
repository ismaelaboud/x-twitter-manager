from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_content_generator import AIContentGenerator
import tweepy
import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

router = APIRouter()
content_generator = AIContentGenerator()

class ContentRequest(BaseModel):
    topic: str = None
    tone: str = 'professional'
    thread_length: int = 3

@router.post("/generate-tweet")
async def generate_tweet(request: ContentRequest) -> dict:
    """
    Generate a tweet using AI
    """
    try:
        tweet = content_generator.generate_tweet(
            topic=request.topic, 
            tone=request.tone
        )
        
        # Optional: Sentiment Analysis
        sentiment = content_generator.analyze_sentiment(tweet)
        
        return {
            "tweet": tweet,
            "sentiment": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-thread")
async def generate_thread(request: ContentRequest) -> dict:
    """
    Generate a Twitter thread using AI
    """
    try:
        thread = content_generator.generate_thread(
            topic=request.topic, 
            length=request.thread_length
        )
        
        return {
            "thread": thread,
            "thread_length": len(thread)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/post-tweet")
async def post_tweet(tweet: str) -> dict:
    """
    Post a tweet to Twitter
    Note: Requires valid Twitter credentials
    """
    try:
        # Initialize Tweepy client (you'll need to replace with actual credentials)
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_CLIENT_ID'), 
            os.getenv('TWITTER_CLIENT_SECRET')
        )
        api = tweepy.API(auth)
        
        # Post tweet
        posted_tweet = api.update_status(tweet)
        
        return {
            "message": "Tweet posted successfully",
            "tweet_id": posted_tweet.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/post-thread")
async def post_thread(thread: List[str]) -> dict:
    """
    Post a thread to Twitter
    """
    try:
        # Initialize Tweepy client
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_CLIENT_ID'), 
            os.getenv('TWITTER_CLIENT_SECRET')
        )
        api = tweepy.API(auth)
        
        # Post first tweet
        first_tweet = api.update_status(thread[0])
        previous_tweet = first_tweet
        
        # Post subsequent tweets as replies
        for tweet_text in thread[1:]:
            reply_tweet = api.update_status(
                status=tweet_text, 
                in_reply_to_status_id=previous_tweet.id
            )
            previous_tweet = reply_tweet
        
        return {
            "message": "Thread posted successfully",
            "first_tweet_id": first_tweet.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
