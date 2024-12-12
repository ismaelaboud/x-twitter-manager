from services.transformer_generator import TransformerTweetGenerator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def generate_tweets():
    # Initialize Transformer Tweet Generator
    generator = TransformerTweetGenerator()
    
    print("🚀 AI Tweet Generator (Hugging Face Transformers) 🐦\n")
    
    # Generate individual tweets
    topics = ["AI Innovation", "Future of Technology", "Startup Ecosystem"]
    for topic in topics:
        print(f"🌟 Topic: {topic}")
        tweet = generator.generate_tweet(prompt=f"Insights about {topic}:")
        print(f"📝 Tweet: {tweet}\n")
    
    # Generate a thread
    print("🧵 Tweet Thread:")
    thread = generator.generate_thread(topic="Digital Transformation", length=3)
    for i, tweet in enumerate(thread, 1):
        print(f"Tweet {i}: {tweet}")

if __name__ == "__main__":
    generate_tweets()
