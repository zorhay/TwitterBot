import tweepy
import auth

api = auth.authentication()


def follow():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        print ("Followed everyone that is following " + user.name)

def get_user_tweets(username, count):
	return api.user_timeline(screen_name = username, count = count, include_rts = True)

def get_urls_from_tweet(tweet):
    urls = tweet._json.get('entities').get('urls')
    return [ url.get('url') for url in urls ]

def clean_tweet_from_urls(tweet_text, urls):
    for url in urls:
        tweet_text = tweet_text.replace(url, '')
    return normalise_tweet(tweet_text)

def clean_tweet_from_usernames(tweet_text):
    for word in tweet_text.split(' '):
        if word.startswith('@'):
            tweet_text = tweet_text.replace(word, '')
    return normalise_tweet(tweet_text)

def normalise_tweet(tweet_text):
    while '  ' in tweet_text:
        tweet_text = tweet_text.replace('  ', ' ')
    return tweet_text.strip()

if __name__ == '__main__':
    print (clean_tweet_from_usernames('dasj dasb dasjdhaj     @sjdbad dhajsdh'))
    # tweets = get_user_tweets('__humanx__', 10)
    # for tweet in tweets:
    #     if tweet._json.get('in_reply_to_status_id') is None:
    #         print(tweet._json.get('text'))


