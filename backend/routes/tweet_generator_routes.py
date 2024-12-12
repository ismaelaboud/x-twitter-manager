from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.transformer_generator import TransformerTweetGenerator

router = APIRouter()
generator = TransformerTweetGenerator()

class TweetGenerationRequest(BaseModel):
    topic: str
    type: str = 'single'
    tone: Optional[str] = 'professional'

class TweetGenerationResponse(BaseModel):
    content: List[str]
    type: str
    character_counts: List[int]

@router.post("/generate-tweet", response_model=TweetGenerationResponse)
async def generate_tweet(request: TweetGenerationRequest):
    try:
        if not request.topic:
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        if request.type == 'single':
            tweet = generator.generate_tweet(
                prompt=f"{request.tone} perspective on {request.topic}"
            )
            content = [tweet]
        elif request.type == 'thread':
            content = generator.generate_thread(
                topic=request.topic, 
                length=3
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid generation type")
        
        return {
            "content": content,
            "type": request.type,
            "character_counts": [len(tweet) for tweet in content]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topic-suggestions")
async def get_topic_suggestions():
    return [
        "AI Innovation",
        "Future of Technology", 
        "Startup Ecosystem",
        "Climate Change",
        "Digital Transformation",
        "Machine Learning Trends",
        "Cybersecurity",
        "Space Exploration",
        "Renewable Energy",
        "Blockchain Technology"
    ]

@router.get("/tone-options")
async def get_tone_options():
    return [
        {"value": "professional", "label": "Professional"},
        {"value": "casual", "label": "Casual"},
        {"value": "witty", "label": "Witty"},
        {"value": "inspirational", "label": "Inspirational"}
    ]
