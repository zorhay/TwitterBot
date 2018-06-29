from auth import api
from operations import *
from datetime import datetime

def save_all_tweet_by_username(screen_name, output_file=None):
    '''
    :param screen_name: user nickname
    :param output_file: tweets store file path
    :return: saved tweet count
    '''

    if output_file is None:
        output_file = '../data/' + screen_name + '.txt'
    count = api.get_user(screen_name).statuses_count

    max_tweet_id = api.user_timeline(screen_name=screen_name, count=1)[0].id

    saved_tweet_count = 0
    while count > 0:
        tweets = api.user_timeline(screen_name=screen_name, count=count, max_id=max_tweet_id)

        if tweets.__len__() == 0:
            break
        else:
            count -= tweets.__len__()

        max_tweet_id = tweets.max_id
        if max_tweet_id is None:
            break

        with open(output_file, 'a') as f:
            for tweet in tweets:
                # TODO optimise
                tweet_text = tweet.text
                urls = get_urls_from_tweet(tweet)
                tweet_text = clean_urls_from_tweet_text(tweet_text, urls)
                tweet_text = clean_usernames_from_tweet_text(tweet_text)
                f.write(tweet_text + '\n')
            print('{} saved.'.format(tweets.__len__()))
            saved_tweet_count += tweets.__len__()
    print(saved_tweet_count)
    return saved_tweet_count


def user_scraper(language='hy', activity=0.25, count=100):
    '''
    :param language: main tweets language
    :param activity: tweets middle consistency (tweet/day)
    :param count: user max count
    :return:
    '''

    # [tweet for tweet in tweepy.Cursor(api.user_timeline, screen_name=name).items()]
    # TODO solve limit problem

    followers = api.friends()
    while count > 0:
        for follower in followers:
            f_fs = follower.followers()
            for f_f in f_fs:
                if not f_f.protected and \
                    check_user_tweet_language(f_f.screen_name) == language and \
                    check_user_activity(f_f.screen_name) > activity:
                    f_f.follow()
                    count -= 1
        break


def check_user_tweet_language(screen_name):
    '''
    :param screen_name: user nickname
    :return: main language of tweets
    '''
    tweets = api.user_timeline(screen_name=screen_name, count=200)
    if not tweets:
        return None

    langs = {}
    for tweet in tweets:
        if langs.get(tweet.lang, None) is None:
            langs[tweet.lang] = 1
        else:
            langs[tweet.lang] += 1

    return max(langs, key=langs.get)


def check_user_activity(screen_name):
    '''
    :param screen_name: user nickname
    :return: tweets middle consistency
    '''
    tweets = api.user_timeline(screen_name=screen_name, count=200)
    if tweets.__len__() < 10 or (datetime.utcnow() - tweets[0].created_at).days > 30:
        return 0

    delta_time = (tweets[0].created_at - tweets[-1].created_at)
    delta_days = delta_time.days + delta_time.seconds / 86400 # 60*60*24
    return tweets.__len__() / delta_days


# TODO create user last readed tweet id and user id table