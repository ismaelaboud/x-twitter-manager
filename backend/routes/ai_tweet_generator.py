from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your tweet generation service
from services.transformer_generator import TransformerTweetGenerator

# Initialize tweet generator
tweet_generator = TransformerTweetGenerator()

# Router for AI Tweet Generation
router = APIRouter(prefix="", tags=["AI Tweet Generation"])

# Request Model
class TweetGenerationRequest(BaseModel):
    topic: str
    tone: Literal['professional', 'casual', 'witty', 'inspirational']
    generationType: Literal['single', 'thread']

# Response Model
class TweetGenerationResponse(BaseModel):
    tweets: List[str]

@router.post("/ai/generate-tweets", response_model=TweetGenerationResponse)
async def generate_ai_tweets(request: TweetGenerationRequest):
    """
    Generate AI tweets based on topic, tone, and generation type
    
    Args:
        request (TweetGenerationRequest): Parameters for tweet generation
    
    Returns:
        TweetGenerationResponse: Generated tweets
    """
    logger.info(f"Received tweet generation request: {request}")
    logger.info(f"Router prefix: {router.prefix}")  # Log the router prefix
    
    try:
        # Validate input
        if not request.topic:
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        # Construct prompt based on tone and topic
        tone_prompts = {
            'professional': f"A professional insight about {request.topic}:",
            'casual': f"A casual take on {request.topic}:",
            'witty': f"A witty observation about {request.topic}:",
            'inspirational': f"An inspirational message related to {request.topic}:"
        }
        
        prompt = tone_prompts.get(request.tone, tone_prompts['professional'])
        
        # Generate tweets based on type
        if request.generationType == 'thread':
            tweets = tweet_generator.generate_thread(
                topic=request.topic, 
                length=3, 
                max_tweet_length=280
            )
        else:
            tweet = tweet_generator.generate_tweet(
                prompt=prompt, 
                max_length=280
            )
            tweets = [tweet]
        
        logger.info(f"Generated tweets: {tweets}")
        return TweetGenerationResponse(tweets=tweets)
    
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error generating tweets: {e}")
        raise HTTPException(status_code=500, detail=str(e))
