import tweepy
from config import credentials

api = tweepy.API()

def authentication(cds=credentials):
    auth = tweepy.OAuthHandler(cds['consumer_key'], cds['consumer_secret'])
    auth.set_access_token(cds['access_token'], cds['access_token_secret'])
    api.auth = auth
    return api