# sentiment_analysis.py
from textblob import TextBlob
import threading

def analyze_sentiment(texts):
    sentiments = []

    def analyze():
        for text in texts:
            analysis = TextBlob(text)
            sentiment_score = analysis.sentiment.polarity
            if sentiment_score > 0:
                sentiments.append("positive")
            elif sentiment_score < 0:
                sentiments.append("negative")
            else:
                sentiments.append("neutral")

    # Create and start the thread for analyzing sentiments
    thread = threading.Thread(target=analyze)
    thread.start()
    thread.join()  # Wait for the thread to finish

    return sentiments
