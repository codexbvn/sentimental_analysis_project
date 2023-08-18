# data_preprocessing.py
import re
import threading

def clean_tweets(tweets):
    cleaned_tweets = []

    def preprocess_tweets():
        for tweet in tweets:
            cleaned_tweet = re.sub(r"http\S+|[^A-Za-z0-9]+", ' ', tweet)
            cleaned_tweets.append(cleaned_tweet)

    # Create and start the thread for preprocessing tweets
    thread = threading.Thread(target=preprocess_tweets)
    thread.start()
    thread.join()  # Wait for the thread to finish

    return cleaned_tweets

