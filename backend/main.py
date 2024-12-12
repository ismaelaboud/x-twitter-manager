import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import bcrypt
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import OAuth routes
from routes.content_routes import router as content_routes_router
from routes.tweet_generator_routes import router as tweet_generator_router
from routes.ai_tweet_generator import router as ai_tweet_generator_router  # Corrected import

# Load environment variables
load_dotenv()

app = FastAPI(title="X-Twitter Bot Backend")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # Backend server
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Optional: Add a middleware to log CORS-related information
@app.middleware("http")
async def log_cors_headers(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    logger.info(f"Response headers: {dict(response.headers)}")
    return response

# Dynamically import Twitter OAuth router if possible
try:
    from routes.twitter_oauth import router as twitter_oauth_router
    app.include_router(twitter_oauth_router, prefix="/auth", tags=["Authentication"])
except ImportError:
    print("Warning: Twitter OAuth router could not be imported. OAuth functionality will be limited.")

# Include other routes
app.include_router(content_routes_router, prefix="/content", tags=["Content Generation"])
app.include_router(tweet_generator_router, prefix="/tweet-generator", tags=["AI Tweet Generation"])

# Log router details before inclusion
logger.info(f"AI Tweet Generator Router: {ai_tweet_generator_router}")
logger.info(f"Router routes: {ai_tweet_generator_router.routes}")

# Explicitly include the router with no prefix
app.include_router(ai_tweet_generator_router)

# User Registration Model
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    @classmethod
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @field_validator('password')
    @classmethod
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# Simulated User Database (replace with actual database in production)
users_db = {}

@app.post("/accounts/register")
async def register_account(user: UserCreate):
    # Check if username or email already exists
    if any(u['username'] == user.username for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if any(u['email'] == user.email for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Store user
    users_db[user.email] = {
        'username': user.username,
        'email': user.email,
        'password': hashed_password
    }
    
    return {"message": "User registered successfully", "username": user.username}

@app.get("/")
async def root():
    return {"message": "Welcome to X-Twitter Bot Backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
