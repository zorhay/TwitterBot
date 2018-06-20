import tweepy
from config import credentials

def authentication(cds=credentials):
    auth = tweepy.OAuthHandler(cds['consumer_key'], cds['consumer_secret'])
    auth.set_access_token(cds['access_token'], cds['access_token_secret'])
    api = tweepy.API(auth)
    return api

if __name__ == '__main__':
    api = authentication()
    user = api.me()
    print (user.name)