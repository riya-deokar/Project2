from textblob import TextBlob

def analyze_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    
    # Get the sentiment polarity
    # The polarity score is a float within the range [-1.0, 1.0]
    sentiment_polarity = blob.sentiment.polarity
    
    # Determine sentiment
    if sentiment_polarity > 0.1:  # Adjust thresholds as necessary
        return 'Positive'
    elif sentiment_polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'
