import tweepy
from config import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    stock_symbol,
    elasticsearch_index
)
from elasticsearch_setup import setup_elasticsearch
from sentiment_analysis import analyze_sentiment

class TwitterStreamer(tweepy.StreamListener):
    def __init__(self, es):
        super().__init__()
        self.es = es

    def on_status(self, status):
        print(status.text)
        sentiment_score = analyze_sentiment(status.text)
        doc = {
            "author": status.user.screen_name,
            "date": status.created_at,
            "message": status.text,
            "sentiment": sentiment_score
        }
        self.es.index(index=elasticsearch_index, document=doc)

    def on_error(self, status_code):
        if status_code == 404:
            print("Error 404: The requested resource does not exist.")
        elif status_code == 420:
            print("Error 420: A rate limit was exceeded. Disconnecting the stream.")
            # Returning False disconnects the stream
            return False
        else:
            print(f"Encountered streaming error (status code: {status_code}). Continuing...")
        # Returning True keeps the stream alive
        return True

def start_streaming(es):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream_listener = TwitterStreamer(es)
    stream = tweepy.Stream(auth=auth, listener=stream_listener)
    stream.filter(track=[stock_symbol], languages=['en'], is_async=True)

if __name__ == '__main__':
    es = setup_elasticsearch()
    start_streaming(es)
