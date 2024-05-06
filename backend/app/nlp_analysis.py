# nlp_analysis.py
import spacy
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load Spacy Model
nlp = spacy.load('en_core_web_sm')

# Keyword extraction using spaCy
def extract_keywords_spacy(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.is_stop != True and token.is_punct != True]

# Sentiment analysis using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return 'positive' if analysis.sentiment.polarity > 0 else 'neutral' if analysis.sentiment.polarity == 0 else 'negative'

# Entity recognition using spaCy
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
