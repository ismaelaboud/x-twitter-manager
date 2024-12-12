import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import re

class TransformerTweetGenerator:
    def __init__(self, model_name="distilgpt2"):
        """
        Initialize Hugging Face Transformer model for tweet generation
        
        Args:
            model_name (str): Hugging Face model to use
        """
        try:
            # Use CPU to avoid CUDA/GPU complications
            self.device = torch.device('cpu')
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
            
            # Configure tokenizer
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Set model to evaluation mode
            self.model.eval()
        
        except Exception as e:
            print(f"🚨 Model Loading Error: {e}")
            self.tokenizer = None
            self.model = None

    def _clean_tweet(self, text, max_length=280):
        """
        Clean and format generated text into a tweet
        """
        # Remove multiple whitespaces and strip
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove URLs and special tokens
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'<.*?>', '', text)
        
        # Truncate to max length
        text = text[:max_length]
        
        # Add hashtag if no hashtag exists
        if not re.search(r'#\w+', text):
            hashtags = ['#Innovation', '#Technology', '#AI', '#Future']
            text += f" {random.choice(hashtags)}"
        
        return text.strip()

    def generate_tweet(self, prompt=None, max_length=280):
        """
        Generate an AI-powered tweet
        """
        if not self.model or not self.tokenizer:
            return "🤖 AI tweet generation currently unavailable."

        # Default prompts if no specific prompt provided
        default_prompts = [
            "The future of technology is",
            "Innovative ideas that are changing the world",
            "Breaking news in artificial intelligence:",
            "A revolutionary concept in tech:"
        ]
        
        # Select or use provided prompt
        current_prompt = prompt or random.choice(default_prompts)
        
        try:
            # Encode the prompt
            input_ids = self.tokenizer.encode(current_prompt, return_tensors='pt').to(self.device)
            
            # Generate text with more controlled randomness
            with torch.no_grad():
                output = self.model.generate(
                    input_ids, 
                    max_length=max_length * 2,  
                    num_return_sequences=3,     
                    no_repeat_ngram_size=2,
                    temperature=0.7,            
                    top_k=50,                   
                    top_p=0.95,
                    do_sample=True
                )
            
            # Decode and clean generated tweets
            tweets = [
                self._clean_tweet(
                    self.tokenizer.decode(seq, skip_special_tokens=True), 
                    max_length
                ) for seq in output
            ]
            
            # Return the most interesting tweet
            return max(tweets, key=len)
        
        except Exception as e:
            print(f"🚨 Tweet Generation Error: {e}")
            return "🤖 Unable to generate tweet at the moment."

    def generate_thread(self, topic=None, length=3, max_tweet_length=280):
        """
        Generate a thread of AI-powered tweets
        """
        thread = []
        for _ in range(length):
            # Use topic as initial prompt if provided
            prompt = f"Continuing the discussion about {topic}:" if topic else None
            tweet = self.generate_tweet(prompt, max_tweet_length)
            thread.append(tweet)
        
        return thread

# Demonstration
if __name__ == "__main__":
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
