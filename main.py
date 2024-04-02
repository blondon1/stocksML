from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from config import *
from sentiment_analysis import analyze_sentiment
from stock_data_fetcher import fetch_stock_data
from elasticsearch_setup import setup_elasticsearch

class TwitterStreamer(StreamListener):
    def on_status(self, status):
        sentiment_score = analyze_sentiment(status.text)
        print(f"Tweet: {status.text}, Sentiment: {sentiment_score}")
        # Here, integrate Elasticsearch to store the tweet and its sentiment score

    def on_error(self, status_code):
        print(f"Error: {status_code}")

def start_streaming():
    listener = TwitterStreamer()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=[stock_symbol], languages=['en'])

if __name__ == '__main__':
    es = setup_elasticsearch()
    start_streaming()
    stock_data = fetch_stock_data(stock_symbol)
    print(stock_data)
    # Integrate Elasticsearch to store stock data
