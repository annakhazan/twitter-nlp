import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
from tweepy import OAuthHandler
import operator
# import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

def findRelatedTweets(topic, last_id, output_count):
    consumer_key = 'kdaidOlBCg8sCTv9EdhhlpRGE'
    consumer_key_secret = 'dN5lryDtZLVyTEelGek2LXaXxsU9eXMc4oP9LbjtqKdpR9RhXy'
    access_token = '1363491181-Vi4vQrFSm3gwtrMbeqTn87cwCg7r8bvRU7MqtFR'
    access_token_secret = '4gEoBWf7z0sPGKwADrH3VrgJT0nuJ9DQra8E6k7O6hYNU'
    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.search(q=topic, count=output_count, since_id=last_id)

def analyzeSentiment(sid, text):
    output = sid.polarity_scores(text)['compound']
    if output > 0.2:
        return ('Positive', output)
    elif output > -0.2 and output < 0.2:
        return ('Neutral', output)
    else:
        return ('Negative', output)

if __name__ == '__main__':
    # input = raw_input('What topic are you interested in? >> ')
    input = 'Trump'
    sid = SentimentIntensityAnalyzer()
    tknzr = TweetTokenizer(strip_handles=True)
    stpwrds = stopwords.words('english')
    counter = 1
    i = 1
    data = []
    word_counts = {}
    retweet_count = 0
    output_count = 100
    result_count = output_count
    pos_count = 0
    neutral_count = 0
    neg_count = 0
    sum_sentiment_scores = 0
    while counter < 5 and result_count == output_count:
        tweets = findRelatedTweets(input, i, output_count)
        for tweet in tweets:
            sentiment = analyzeSentiment(sid, tweet.text)
            print tknzr.tokenize(tweet.text)
            tweet.text[:2] == 'RT'
            if tweet.text[:2] == 'RT':
                retweet = True
                retweet_count += 1
            else:
                retweet = False
            if sentiment[0] == 'Positive':
                pos_count += 1
            elif sentiment[0] == 'Neutral':
                neutral_count += 1
            else:
                neg_count += 1
            sum_sentiment_scores += sentiment[1]
            for word in tweet.text.split(' '):
                if word.lower() not in stpwrds and word.lower() != input.lower():
                    if word.lower() in word_counts:
                        word_counts[word.lower()] += 1
                    else:
                        word_counts[word.lower()] = 1
            data.append({'id':tweet.id, 'text':tweet.text, 'sentiment':sentiment, 'retweet':retweet})
            i = tweet.id
            counter += 1
            result_count = len(tweets)
    total_tweets = len(data)
    common_words = sorted(word_counts.items(), key=operator.itemgetter(1))[-20:]
    average_sentiment = sum_sentiment_scores/total_tweets
    print 'Total recent tweets: {0}'.format(total_tweets)
    print 'Top 20 related words: {0}'.format(common_words)
    print 'Average Sentiment (ranging from -1 to 1): {0}'.format(average_sentiment)
