import time
import tweepy
import auth
from operations import *
from crawler import *

api = auth.authentication()


def main():
    while True:
        try:
            tweet_scraper()
            break
        except tweepy.RateLimitError as e:
            print(e, '\nwait 15 minutes')
            time.sleep(15 * 60)


if __name__ == '__main__':
    main()
