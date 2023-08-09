# app.py
from flask import Flask, render_template, request, jsonify, url_for
import threading

app = Flask(__name__)

# Import the functions from other files
from data_collection.data_collection import fetch_tweets
from data_preprocessing.data_preprocessing import clean_tweets
from sentiment_analysis.sentiment_analysis import analyze_sentiment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    keyword = request.form['keyword']
    tweets = fetch_tweets(keyword)
    
    # Create threads for data preprocessing and sentiment analysis
    preprocessing_thread = threading.Thread(target=clean_tweets, args=(tweets,))
    sentiment_analysis_thread = threading.Thread(target=analyze_sentiment, args=(tweets,))

    preprocessing_thread.start()
    sentiment_analysis_thread.start()

    preprocessing_thread.join()
    sentiment_analysis_thread.join()

    cleaned_tweets = clean_tweets(tweets)
    sentiments = analyze_sentiment(cleaned_tweets)

    return render_template('results.html', keyword=keyword, tweets=tweets, sentiments=sentiments)

@app.route('/sentiment_data')
def sentiment_data():
    # Retrieve the analyzed sentiments
    keyword = request.form['keyword']
    tweets = fetch_tweets(keyword)
    cleaned_tweets = clean_tweets(tweets)
    sentiments = analyze_sentiment(cleaned_tweets)

    # Count the occurrences of each sentiment
    sentiment_counts = {
        'positive': sentiments.count('positive'),
        'neutral': sentiments.count('neutral'),
        'negative': sentiments.count('negative')
    }

    return jsonify(sentiment_counts)

if __name__ == '__main__':
    app.run(debug=True)

