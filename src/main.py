import time
from tweepy import RateLimitError
from bot_api import authentication, TweetScraper

api = authentication()


def main():
    tweet_scraper = TweetScraper(api=api)
    while True:
        try:
            tweet_scraper.run()
            break
        except RateLimitError as e:
            print(e, '\nwait 15 minutes')
            time.sleep(15 * 60)


if __name__ == '__main__':
    main()
