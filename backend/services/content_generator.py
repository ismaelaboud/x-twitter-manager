import random
from typing import List, Optional
import markovify
import nltk
from textblob import TextBlob

class ContentGenerator:
    def __init__(self):
        # Download necessary NLTK data
        nltk.download('punkt', quiet=True)
        
        # Predefined content templates
        self.templates = [
            "Exciting news! {content}",
            "Just thinking about {content}",
            "Hot take: {content}",
            "Breaking: {content}"
        ]
        
        # Sample training data (can be expanded)
        self.training_data = [
            "Technology is changing the world rapidly.",
            "Innovation drives progress in unexpected ways.",
            "The future is full of incredible possibilities.",
            "Learning never stops in our dynamic world."
        ]
    
    def generate_tweet(self, 
                       topic: Optional[str] = None, 
                       max_length: int = 280, 
                       style: str = 'casual') -> str:
        """
        Generate a tweet with optional topic and style
        
        :param topic: Optional specific topic for the tweet
        :param max_length: Maximum tweet length
        :param style: Tweet style (casual, professional, etc.)
        :return: Generated tweet text
        """
        if topic:
            # Generate content based on topic
            base_content = f"Thoughts on {topic}: " + self._generate_markov_text(topic)
        else:
            # Generate random content
            base_content = self._generate_markov_text()
        
        # Apply template
        tweet = random.choice(self.templates).format(content=base_content)
        
        # Truncate to max length
        return tweet[:max_length]
    
    def _generate_markov_text(self, seed: Optional[str] = None, length: int = 50) -> str:
        """
        Generate text using Markov chain
        
        :param seed: Optional seed text
        :param length: Desired text length
        :return: Generated text
        """
        try:
            # Use seed or training data
            text_model = markovify.Text(self.training_data)
            generated_text = text_model.make_short_sentence(length) or random.choice(self.training_data)
            return generated_text
        except Exception:
            return random.choice(self.training_data)
    
    def generate_thread(self, 
                        topic: str, 
                        num_tweets: int = 3, 
                        max_length: int = 280) -> List[str]:
        """
        Generate a tweet thread on a specific topic
        
        :param topic: Thread topic
        :param num_tweets: Number of tweets in the thread
        :param max_length: Maximum length per tweet
        :return: List of tweet texts
        """
        thread = []
        for i in range(num_tweets):
            tweet = self.generate_tweet(topic, max_length)
            thread.append(tweet)
        return thread
    
    def generate_reply(self, 
                       original_tweet: str, 
                       sentiment: str = 'neutral') -> str:
        """
        Generate a contextual reply based on original tweet
        
        :param original_tweet: Tweet to reply to
        :param sentiment: Desired reply sentiment
        :return: Reply text
        """
        # Analyze original tweet sentiment
        blob = TextBlob(original_tweet)
        original_sentiment = blob.sentiment.polarity
        
        # Generate reply based on sentiment
        if sentiment == 'positive':
            reply_template = [
                "Great point! {content}",
                "Absolutely agree! {content}",
                "Couldn't have said it better myself. {content}"
            ]
        elif sentiment == 'negative':
            reply_template = [
                "I respectfully disagree. {content}",
                "There's another perspective to consider: {content}",
                "While I see your point, {content}"
            ]
        else:
            reply_template = [
                "Interesting thought. {content}",
                "That's an intriguing perspective. {content}",
                "Some additional context: {content}"
            ]
        
        # Generate reply
        reply_content = self._generate_markov_text(original_tweet)
        reply = random.choice(reply_template).format(content=reply_content)
        
        return reply[:280]  # Ensure tweet length
