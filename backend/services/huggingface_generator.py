import random
import re

class HuggingFaceContentGenerator:
    def __init__(self):
        """
        Initialize content generator with predefined templates
        """
        self.topics = [
            "Technology", 
            "Innovation", 
            "Personal Growth", 
            "Future Trends",
            "AI",
            "Startup Culture",
            "Digital Transformation"
        ]
        
        self.tone_templates = {
            'professional': [
                "Exploring the cutting edge of {topic}: {insight}",
                "Key insights on {topic} that are reshaping industries.",
                "Strategic perspective on the evolving landscape of {topic}."
            ],
            'casual': [
                "Just thinking about how {topic} is changing everything! ",
                "Random thought: {topic} is pretty amazing right now.",
                "Anyone else excited about the potential of {topic}?"
            ],
            'witty': [
                "Breaking news: {topic} just got interesting! ",
                "{topic} walks into a bar... and changes everything. ",
                "Plot twist: {topic} is the hero we didn't know we needed."
            ]
        }

    def _clean_tweet(self, text, max_length=280):
        """
        Clean and format generated text into a tweet
        """
        # Remove multiple whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Truncate to max length
        text = text[:max_length]
        
        # Add hashtag if no hashtag exists
        if not re.search(r'#\w+', text):
            hashtags = ['#Innovation', '#Technology', '#AI', '#Future']
            text += f" {random.choice(hashtags)}"
        
        return text.strip()

    def generate_tweet(self, topic=None, tone='professional', max_length=280):
        """
        Generate a tweet-like text
        """
        # Select topic if not provided
        selected_topic = topic or random.choice(self.topics)
        
        # Select tone templates
        tone_options = self.tone_templates.get(tone, self.tone_templates['professional'])
        
        # Generate tweet template
        tweet_template = random.choice(tone_options)
        
        # Generate insights
        insights = [
            "Driving innovation forward",
            "Transforming the way we work",
            "Unlocking new possibilities",
            "Challenging the status quo",
            "Empowering future generations"
        ]
        
        # Format tweet
        tweet = tweet_template.format(
            topic=selected_topic,
            insight=random.choice(insights)
        )
        
        # Clean and return tweet
        return self._clean_tweet(tweet, max_length)

    def generate_thread(self, topic=None, length=3, max_tweet_length=280):
        """
        Generate a thread of tweets
        """
        thread = []
        for _ in range(length):
            tweet = self.generate_tweet(topic, max_length=max_tweet_length)
            thread.append(tweet)
        
        return thread

# Example usage
if __name__ == "__main__":
    generator = HuggingFaceContentGenerator()
    
    # Generate a tweet
    tweet = generator.generate_tweet(topic="AI")
    print("Generated Tweet:", tweet)
    
    # Generate a thread
    thread = generator.generate_thread(topic="Technology", length=3)
    print("Generated Thread:", thread)
