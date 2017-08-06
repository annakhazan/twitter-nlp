import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
from tweepy import OAuthHandler

def findRelatedTweets(topic, last_id):
    consumer_key = 'kdaidOlBCg8sCTv9EdhhlpRGE'
    consumer_key_secret = 'dN5lryDtZLVyTEelGek2LXaXxsU9eXMc4oP9LbjtqKdpR9RhXy'
    access_token = '1363491181-Vi4vQrFSm3gwtrMbeqTn87cwCg7r8bvRU7MqtFR'
    access_token_secret = '4gEoBWf7z0sPGKwADrH3VrgJT0nuJ9DQra8E6k7O6hYNU'
    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.search(q=topic, count=100, since_id=last_id)

def analyzeSentiment(sid, text):
    if sid.polarity_scores(text)['compound'] > 0.2:
        return 'Positive'
    elif sid.polarity_scores(text)['compound'] > -0.2 and sid.polarity_scores(text)['compound'] < 0.2:
        return 'Neutral'
    else:
        return 'Negative'

if __name__ == '__main__':
    # input = raw_input('What topic are you interested in? >> ')
    input = 'Trump'
    sid = SentimentIntensityAnalyzer()
    counter = 1
    i = 1
    data = []
    while counter < 11:
        tweets = findRelatedTweets(input, i)
        for tweet in tweets:
            sentiment = analyzeSentiment(sid, tweet.text)
            retweet = tweet.text[:2] == 'RT'
            print tweet.text
            print retweet
            print ''
            data.append({'id':tweet.id, 'text':tweet.text, 'sentiment':sentiment, 'retweet':retweet})
            i = tweet.id
        counter += 1
