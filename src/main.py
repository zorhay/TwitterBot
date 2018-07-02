import time
import tweepy
import auth
from operations import *
from crawler import *


api = auth.authentication()

def main():
    run_flag = True
    while run_flag:
        try:
            tweet_scraper()
            run_flag = False
        except tweepy.RateLimitError as e:
            print(e, '\nwait 15 minutes')
            time.sleep(15 * 60)




if __name__ == '__main__':
    main()