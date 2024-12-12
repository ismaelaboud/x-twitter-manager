import os
from dotenv import load_dotenv
from services.huggingface_generator import HuggingFaceContentGenerator

# Load environment variables
load_dotenv()

def test_content_generation():
    """
    Test content generation capabilities
    """
    try:
        # Initialize generator
        generator = HuggingFaceContentGenerator()
        
        # Test tweet generation with different topics and tones
        topics = ["AI", "Technology", "Innovation"]
        tones = ['professional', 'casual', 'witty']
        
        print("🚀 Testing Tweet Generation:")
        for topic in topics:
            for tone in tones:
                tweet = generator.generate_tweet(topic=topic, tone=tone)
                print(f"Topic: {topic}, Tone: {tone}")
                print(f"Tweet: {tweet}")
                print("---")
        
        # Test thread generation
        print("\n🧵 Testing Thread Generation:")
        thread_topics = ["Future of Work", "Digital Transformation"]
        for topic in thread_topics:
            thread = generator.generate_thread(topic=topic, length=3)
            print(f"Thread Topic: {topic}")
            for i, tweet in enumerate(thread, 1):
                print(f"Tweet {i}: {tweet}")
            print("---")
        
        return True
    
    except Exception as e:
        print(f"❌ Content Generation Failed: {e}")
        return False

if __name__ == "__main__":
    test_content_generation()
