from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(tweet_text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(tweet_text)
    return sentiment_score['compound']
