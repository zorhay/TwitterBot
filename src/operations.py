from auth import api
import tweepy

def _normalise_tweet(tweet_text):
    while '  ' in tweet_text:
        tweet_text = tweet_text.replace('  ', ' ')
    return tweet_text.strip()

def get_user_tweets(username, count):
    return api.user_timeline(screen_name = username, count = count, include_rts = True)

def get_urls_from_tweet(tweet):
    urls = tweet._json.get('entities').get('urls')
    return [url.get('url') for url in urls]

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