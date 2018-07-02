import tweepy
import re
from auth import api

def _normalise_tweet(tweet_text):
    while '  ' in tweet_text:
        tweet_text = tweet_text.replace('  ', ' ')
    return tweet_text.strip()

def get_user_tweets(username, count):
    return api.user_timeline(screen_name = username, count = count, include_rts = False)

def get_urls_from_tweet(tweet):
    urls = tweet._json.get('entities').get('urls')
    media_urls = tweet._json.get('entities').get('media')
    return [url.get('url') for url in urls + media_urls]

def clean_urls_from_tweet_text(tweet_text, urls):
    for url in urls:
        tweet_text = tweet_text.replace(url, '')
    return _normalise_tweet(tweet_text)

def clean_usernames_from_tweet_text(tweet_text):
    for word in tweet_text.split(' '):
        if word.startswith('@'):
            tweet_text = tweet_text.replace(word, '')
    return _normalise_tweet(tweet_text)

def follow_all_followers():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

def get_not_reply_tweets(tweets):
    return [tweet for tweet in tweets if tweet._json.get('in_reply_to_status_id') is None]

def tweet_is_not_complete(tweet_text):
    return not tweet_text.strip().endswith(('.', '։', ':'))

def has_url(tweet):
    urls = tweet._json.get('entities').get('urls')
    for url in urls:
        if url.get('url') is not None:
            return True
    return False

def print_not_complete_tweets(username, count):
    tweets = get_user_tweets(username, count)
    for tweet in tweets:
        tweet_text = get_text_from_tweet(tweet)
        if (not has_url(tweet)) and tweet_is_not_complete(tweet_text):
            print(tweet_text)

def tweet_processing(tweet):
    if tweet.lang != 'hy':
        return None

    tweet_text = tweet.text
    #clean usernames
    # usernames = ['@' + user_mention.get('screen_name') for user_mention in tweet._json.get('entities').get('user_mentions')]
    # for username in usernames:
    #     tweet_text = tweet_text.replace(username, '')
    #
    # #clean urls
    # urls = tweet._json.get('entities').get('urls')
    # media_urls = tweet._json.get('entities').get('media')
    # if media_urls is None:
    #     media_urls = []
    # all_urls = [url.get('url') for url in urls + media_urls]
    # for url in all_urls:
    #     tweet_text = tweet_text.replace(url, '')
    #
    # return tweet_text

    #hard clean
    tweet_text = re.sub(r'[^ա-ֆԱ-Ֆ ,․։"«»՝՜՞՛]', '', tweet_text)
    return _normalise_tweet(tweet_text)

