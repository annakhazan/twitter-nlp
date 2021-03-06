import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
from tweepy import OAuthHandler
import operator
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
import os

stpwrds = stopwords.words('english')
punctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '...']

# nltk.download()

def findRelatedTweets(topic, last_id, output_len):
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_key_secret = os.environ['TWITTER_CONSUMER_KEY_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.search(q=topic, count=output_len, since_id=last_id)

def analyzeSentiment(sid, text):
    output = sid.polarity_scores(text)['compound']
    if output > 0.2:
        return ('Positive', output)
    elif output > -0.2 and output < 0.2:
        return ('Neutral', output)
    else:
        return ('Negative', output)

def labelRetweet(text):
    return text == 'RT'

def wordMatchesCriteria(word):
    return not(word in stpwrds or word == input.lower() or word == 'rt' or word in punctuation)

def testForValidWord(word):
    try:
        return type(str(word)) is str
    except:
        return False

def updateWordCounts(word_counts, text):
    for word in text:
        word = word.lower()
        if testForValidWord(word) and wordMatchesCriteria(word):
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
    return word_counts

def formatWordCounts(word_counts):
    output = ''
    common_words = sorted(word_counts.items(), key=operator.itemgetter(1))[-20:]
    for w in sorted(common_words, key=lambda v:v[1], reverse=True):
        output += '\t\t' + str(w[0]) + ' (' + str(w[1]) + ' instances),\n'
    return output[:-2]

def summarizeData(tweets):
    unique_users = []
    retweet_count = 0
    pos_count = 0
    neg_count = 0
    sum_sentiments = 0
    word_counts = {}
    for t in tweets:
        unique_users.append(t['user'])
        if t['retweet']:
            retweet_count += 1
        if t['sentiment'][0] == 'Positive':
            pos_count += 1
        elif t['sentiment'][0] == 'Negative':
            neg_count += 1
        sum_sentiments += t['sentiment'][1]
        word_counts = updateWordCounts(word_counts, t['tokenized_text'])
    word_counts = formatWordCounts(word_counts)
    avg_sentiment = sum_sentiments/len(tweets)
    unique_users = set(unique_users)
    return (len(tweets), unique_users, retweet_count, pos_count, neg_count, avg_sentiment, word_counts)

def printOutput(data):
    total_tweets, unique_users, retweet_count, pos_count, neg_count, avg_sentiment, common_words = summarizeData(data)
    print """
        Selected Topic: {0}
        Total Recent Tweets: {1}
        Total Original Tweets: {2}
        Total Retweets: {3}
        Positive Tweets: {4}
        Negative Tweets: {5}
        Average Sentiment (Ranging from -1 to 1): {6}
        Total Unique Users Tweeting: {7}
        Top 20 Related Words:
    {8}
    """.format(input, total_tweets, total_tweets - retweet_count, retweet_count, pos_count, neg_count, avg_sentiment, len(unique_users), common_words)

def writeOutput(data):
    with open('./data/Twitter Activity Related To {0}.csv'.format(input), 'wb+') as f:
        writer = csv.writer(f)
        i = 0
        for row in data:
            if i == 0:
                writer.writerow(['ID', 'Original Text', 'Retweet', 'Sentiment Score', 'Sentiment Analysis', 'User'])
            else:
                try:
                    writer.writerow([
                        row['id'],
                        row['original_text'],
                        row['retweet'],
                        row['sentiment'][0],
                        row['sentiment'][1],
                        row['user']
                    ])
                except:
                    continue
            i+=1

def processTweets(input):
    sid = SentimentIntensityAnalyzer()
    tknzr = TweetTokenizer(strip_handles=True)
    counter = 1
    i = 1
    output_len = 100
    result_count = output_len
    data = []
    while counter < 11 and result_count == output_len:
        tweets = findRelatedTweets(input, i, output_len)
        for tweet in tweets:
            data.append({
                'id':tweet.id,
                'original_text':tweet.text,
                'tokenized_text':tknzr.tokenize(tweet.text),
                'user':tweet.user.id_str,
                'sentiment':analyzeSentiment(sid, tweet.text),
                'retweet':labelRetweet(tknzr.tokenize(tweet.text)[0])
            })
            i = tweet.id
        result_count = len(tweets)
        counter += 1
    writeOutput(data)
    printOutput(data)

if __name__ == '__main__':
    input = raw_input('What topic are you interested in? >> ')
    processTweets(input)
