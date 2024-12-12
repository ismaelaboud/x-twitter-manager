import os
import random
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from textblob import TextBlob

# Import Hugging Face generator as fallback
from .huggingface_generator import HuggingFaceContentGenerator

# Load environment variables
load_dotenv()

class AIContentGenerator:
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize Hugging Face generator as fallback
        self.huggingface_generator = HuggingFaceContentGenerator()
        
        if not api_key:
            print(" OpenAI API Key not set. Falling back to Hugging Face.")
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as e:
                print(f"OpenAI initialization error: {e}")
                self.client = None

    def generate_tweet(self, topic: str = None, tone: str = 'professional') -> str:
        """
        Generate a tweet with fallback to Hugging Face
        """
        if self.client:
            try:
                # Existing OpenAI tweet generation logic
                tones = {
                    'professional': "Use a formal, informative tone.",
                    'casual': "Use a friendly, conversational tone.",
                    'witty': "Use humor and clever wordplay."
                }
                
                prompt = f"""Generate a compelling tweet about {topic or 'Technology'}. 
                {tones.get(tone, tones['professional'])} 
                Ensure the tweet is engaging and under 280 characters."""
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a social media content generator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=280
                )
                tweet = response.choices[0].message.content.strip()
                return tweet
            except Exception as e:
                print(f"OpenAI tweet generation failed: {e}")
        
        # Fallback to Hugging Face
        return self.huggingface_generator.generate_tweet(topic, tone)

    def generate_thread(self, topic: str = None, length: int = 3) -> List[str]:
        """
        Generate a thread with fallback to Hugging Face
        """
        if self.client:
            try:
                # Existing OpenAI thread generation logic
                prompt = f"""Create a {length}-tweet thread about {topic or 'Technology'}. 
                Each tweet should build upon the previous one, 
                creating a coherent narrative. Ensure each tweet 
                is engaging and under 280 characters."""
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a thread content generator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=840
                )
                thread_text = response.choices[0].message.content.strip().split('\n')
                
                # Ensure we have exactly 'length' tweets
                thread_text = thread_text[:length]
                
                return thread_text
            except Exception as e:
                print(f"OpenAI thread generation failed: {e}")
        
        # Fallback to Hugging Face
        return self.huggingface_generator.generate_thread(topic, length)

    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment using TextBlob
        """
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'sentiment': 'positive' if blob.sentiment.polarity > 0 
                         else 'negative' if blob.sentiment.polarity < 0 
                         else 'neutral'
        }

# Example usage
if __name__ == "__main__":
    generator = AIContentGenerator()
    
    # Generate a tweet
    tweet = generator.generate_tweet(topic="AI Ethics")
    print("Generated Tweet:", tweet)
    
    # Generate a thread
    thread = generator.generate_thread(topic="Startup Challenges")
    print("Generated Thread:", thread)
    
    # Sentiment Analysis
    sentiment = generator.analyze_sentiment(tweet)
    print("Sentiment Analysis:", sentiment)
