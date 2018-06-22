import tweepy
import auth
from operations import *

auth.authentication()

def print_not_complete_tweets(username, count):
    tweets = get_user_tweets(username, count)
    for tweet in tweets:
        tweet_text = get_text_from_tweet(tweet)
        if (not has_url(tweet)) and tweet_is_not_complete(tweet_text):
            print(tweet_text)


if __name__ == '__main__':
    print_not_complete_tweets('some_nick', 10) 