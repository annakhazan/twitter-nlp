import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
from tweepy import OAuthHandler
import operator
import stopwords

def findRelatedTweets(topic, last_id):
    consumer_key = 'kdaidOlBCg8sCTv9EdhhlpRGE'
    consumer_key_secret = 'dN5lryDtZLVyTEelGek2LXaXxsU9eXMc4oP9LbjtqKdpR9RhXy'
    access_token = '1363491181-Vi4vQrFSm3gwtrMbeqTn87cwCg7r8bvRU7MqtFR'
    access_token_secret = '4gEoBWf7z0sPGKwADrH3VrgJT0nuJ9DQra8E6k7O6hYNU'
    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.search(q=topic, count=10, since_id=last_id)

def analyzeSentiment(sid, text):
    if sid.polarity_scores(text)['compound'] > 0.2:
        return 'Positive'
    elif sid.polarity_scores(text)['compound'] > -0.2 and sid.polarity_scores(text)['compound'] < 0.2:
        return 'Neutral'
    else:
        return 'Negative'

if __name__ == '__main__':
    print stopwords
    # input = raw_input('What topic are you interested in? >> ')
    input = 'Trump'
    sid = SentimentIntensityAnalyzer()
    counter = 1
    i = 1
    data = []
    word_counts = {}
    while counter < 5:
        tweets = findRelatedTweets(input, i)
        for tweet in tweets:
            print tweet.text
            sentiment = analyzeSentiment(sid, tweet.text)
            retweet = tweet.text[:2] == 'RT'
            for word in tweet.text.split(' '):
                if word.lower() in word_counts:
                    word_counts[word.lower()] += 1
                else:
                    word_counts[word.lower()] = 1
            data.append({'id':tweet.id, 'text':tweet.text, 'sentiment':sentiment, 'retweet':retweet})
            i = tweet.id
            counter += 1
    print sorted(word_counts.items(), key=operator.itemgetter(1))[-5:]
