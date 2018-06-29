import tweepy
import auth
from operations import *
from crawler import *

auth.authentication()

if __name__ == '__main__':
    # save_all_tweet_by_username('__humanx__')
    user_scraper(count=1000)
    # show_friendship
    pass