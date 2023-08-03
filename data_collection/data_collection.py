# data_collection.py
import tweepy
import threading

# Set up Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def fetch_tweets(keyword, num_tweets=100):
    tweets = []

    def collect_tweets():
        for tweet in tweepy.Cursor(api.search, q=keyword, lang="en", tweet_mode="extended").items(num_tweets):
            tweets.append(tweet.full_text)

    # Create and start the thread for fetching tweets
    thread = threading.Thread(target=collect_tweets)
    thread.start()
    thread.join()  # Wait for the thread to finish

    return tweets
