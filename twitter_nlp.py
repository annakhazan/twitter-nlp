import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
from tweepy import OAuthHandler
import operator
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

input = 'Trump'
stpwrds = stopwords.words('english')
punctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '...']

def findRelatedTweets(topic, last_id, output_len):
    consumer_key = 'kdaidOlBCg8sCTv9EdhhlpRGE'
    consumer_key_secret = 'dN5lryDtZLVyTEelGek2LXaXxsU9eXMc4oP9LbjtqKdpR9RhXy'
    access_token = '1363491181-Vi4vQrFSm3gwtrMbeqTn87cwCg7r8bvRU7MqtFR'
    access_token_secret = '4gEoBWf7z0sPGKwADrH3VrgJT0nuJ9DQra8E6k7O6hYNU'
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

def updateWordCounts(word_counts, text):
    for word in text:
        word = word.lower()
        try:
            word_string = str(word)
            if wordMatchesCriteria(word):
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
        except:
            continue
    return word_counts

def formatWordCounts(word_counts):
    output = ''
    common_words = sorted(word_counts.items(), key=operator.itemgetter(1))[-20:]
    for w in sorted(common_words, key=lambda v:v[1], reverse=True):
        output += '\t\t' + str(w[0]) + ' (' + str(w[1]) + ' instances),\n'
    return output

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
        word_counts = updateWordCounts(word_counts, t['text'])
    word_counts = formatWordCounts(word_counts)
    avg_sentiment = sum_sentiments/len(tweets)
    unique_users = set(unique_users)
    print len(tweets)
    return (len(tweets), unique_users, retweet_count, pos_count, neg_count, avg_sentiment, word_counts)

def processTweets(input):
    sid = SentimentIntensityAnalyzer()
    tknzr = TweetTokenizer(strip_handles=True)
    counter = 1
    i = 1
    output_len = 100
    result_count = output_len
    data = []
    while counter < 5 and result_count == output_len:
        tweets = findRelatedTweets(input, i, output_len)
        for tweet in tweets:
            data.append({
                'id':tweet.id,
                'text':tknzr.tokenize(tweet.text),
                'user':tweet.user.id_str,
                'sentiment':analyzeSentiment(sid, tweet.text),
                'retweet':labelRetweet(tknzr.tokenize(tweet.text)[0])
            })
            i = tweet.id
        result_count = len(tweets)
        counter += 1
    return summarizeData(data)

if __name__ == '__main__':
    input = raw_input('What topic are you interested in? >> ')
    total_tweets, unique_users, retweet_count, pos_count, neg_count, avg_sentiment, common_words = processTweets(input)
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
