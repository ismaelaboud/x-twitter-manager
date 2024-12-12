from textblob import TextBlob
from typing import Dict, List, Optional
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

class SentimentService:
    def __init__(self):
        # Download necessary NLTK data
        nltk.download('vader_lexicon', quiet=True)
        
        # Initialize sentiment analyzers
        self.textblob_analyzer = TextBlob
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using multiple methods
        
        :param text: Text to analyze
        :return: Sentiment scores
        """
        # TextBlob sentiment analysis
        blob_sentiment = self.textblob_analyzer(text)
        
        # VADER sentiment analysis
        vader_sentiment = self.vader_analyzer.polarity_scores(text)
        
        return {
            'textblob_polarity': blob_sentiment.sentiment.polarity,
            'textblob_subjectivity': blob_sentiment.sentiment.subjectivity,
            'vader_positive': vader_sentiment['pos'],
            'vader_negative': vader_sentiment['neg'],
            'vader_neutral': vader_sentiment['neu'],
            'vader_compound': vader_sentiment['compound']
        }
    
    def classify_sentiment(self, text: str) -> str:
        """
        Classify sentiment as positive, negative, or neutral
        
        :param text: Text to classify
        :return: Sentiment classification
        """
        sentiment_scores = self.analyze_sentiment(text)
        
        # Use VADER compound score for classification
        compound_score = sentiment_scores['vader_compound']
        
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def batch_sentiment_analysis(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        Perform sentiment analysis on multiple texts
        
        :param texts: List of texts to analyze
        :return: List of sentiment analysis results
        """
        return [self.analyze_sentiment(text) for text in texts]
    
    def generate_reply_based_on_sentiment(self, 
                                          original_text: str, 
                                          sentiment_type: Optional[str] = None) -> str:
        """
        Generate a contextual reply based on sentiment
        
        :param original_text: Original text to reply to
        :param sentiment_type: Optional forced sentiment type
        :return: Generated reply text
        """
        # Determine sentiment if not specified
        if not sentiment_type:
            sentiment_type = self.classify_sentiment(original_text)
        
        # Reply templates based on sentiment
        reply_templates = {
            'positive': [
                "Great perspective! {original}",
                "I totally agree! {original}",
                "Wonderful insight! {original}"
            ],
            'negative': [
                "I understand your concern. {original}",
                "Let's look at this differently. {original}",
                "I hear you, and here's another view: {original}"
            ],
            'neutral': [
                "Interesting point. {original}",
                "That's an intriguing observation. {original}",
                "Some additional context: {original}"
            ]
        }
        
        # Select a random template and format
        import random
        template = random.choice(reply_templates.get(sentiment_type, reply_templates['neutral']))
        
        return template.format(original=original_text)[:280]  # Ensure tweet length
