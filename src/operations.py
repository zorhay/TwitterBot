
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
