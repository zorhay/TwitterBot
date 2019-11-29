import re
import tweepy
from .auth import api


def remove_spaces(tweet_text):
    return " ".join(tweet_text.strip())


def get_urls_from_tweet(tweet):
    urls = tweet._json.get('entities').get('urls')
    return [url.get('url') for url in urls]


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
        if url.get('url'):
            return True
    return False


def get_not_complete_tweets(username, count):
    tweets = api.user_timeline(screen_name=username, count=count, include_rts=True)
    not_complete_tweets = []
    for tweet in tweets:
        tweet_text = textify_tweet(tweet)
        if (not has_url(tweet)) and tweet_is_not_complete(tweet_text):
            not_complete_tweets.append(tweet_text)
    return not_complete_tweets


def textify_tweet(tweet):
    if tweet.lang != 'hy':
        return None
    tweet_text = tweet.text
    tweet_text = re.sub(r'[^ա-ֆԱ-Ֆ ,․։"«»՝՜՞՛]', '', tweet_text)
    return remove_spaces(tweet_text)


def jsonify_tweet(tweet):
    if tweet.lang != 'hy':
        return None
    tweet_text = remove_spaces(re.sub(r'[^ա-ֆԱ-Ֆ ,․։"«»՝՜՞՛]', '', tweet.text))

    return {
        "name": tweet.author.name,
        "screen_name": tweet.author.screen_name,
        "text": tweet_text,
        "hashtags": tweet.entities.get('hashtags'),
        "is_reply": tweet.in_reply_to_status_id is not None,
        "create_time": str(tweet.created_at),
        "language": tweet.lang
            }
