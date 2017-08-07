# Recent Twitter Activity Sentiment Analysis

## To run this program, you must first install the following modules:

#### Natural Language Tool Kit
* `pip install nltk`
* If this is your first time running this script, you'll need to uncomment line 15 in `app/twitter_nlp.py` to download the necessary resources to run the rest of the script.

#### Tweepy, a python wrapper for the Twitter API
* `pip install tweepy`

## Your system must also meet the following requirements:
* Python 2.X
* Instructions are for setup on a Mac

## Registing a Twitter application and setting up environment variables

* Register a Twitter application at apps.twitter.come by going to 'Create an application' and then following the prompts until you get to the 'Keys and Access Tokens' page.
* Next, run `vi ~/.bash_profile` in the command line
* Save `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_KEY_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET` as environment variables.

## Getting Started

* To run this program, run `git clone git@github.com:annakhazan/twitter-nlp.git` in the command line
* Then, type `cd twitter-nlp` to move to the program repository on your local machine.
* Next, type `python app/twitter_nlp.py` to run the program.
* The program will prompt you to enter a subject you're interested in to run the analysis (to start, try `>>> Trump` or `>>> Tesla`).
* In addition to the summary that will be displayed in the command line, you can also find detailed information on each of the relevant tweets in the `data` folder of your local repository.
