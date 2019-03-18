import tweepy
from auth import api
from operations import *
from datetime import datetime
from helpers import *


def tweet_scraper():
    scraped_ids_file = '../other/scrap_ids.txt'
    user_ids = api.friends_ids()
    with open(scraped_ids_file, 'r') as f:
        scraped_ids = f.readlines()

    bad_chars = ['\n', '\'', '\"', '\\']
    for i in range(len(scraped_ids)):
        for bad_char in bad_chars:
            scraped_ids[i] = scraped_ids[i].strip(bad_char)
        scraped_ids[i] = int(scraped_ids[i])

    for user_id in list(set(user_ids) - set(scraped_ids)):
        try:
            user = api.get_user(id=user_id)
        except tweepy.error.TweepError:
            continue

        save_all_tweet_json_by_username(user.screen_name)
        with open(scraped_ids_file, 'a') as f:
            f.write(user.id_str + '\n')


def save_all_tweet_by_username(screen_name, output_file=None):
    '''
    :param screen_name: user nickname
    :param output_file: tweets store file path
    :return: saved tweet count
    '''

    # TODO solve limit problem

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
                tweet_text = tweet_processing(tweet)
                if tweet_text:
                    f.write(tweet_text + '\n')

            print('{} saved.'.format(tweets.__len__()))
            saved_tweet_count += tweets.__len__()
    print(screen_name, saved_tweet_count)
    return saved_tweet_count


def save_all_tweet_json_by_username(screen_name, output_file=None):
    '''
    :param screen_name: user nickname
    :param output_file: tweets store file path
    :return: saved tweet count
    '''

    # TODO solve limit problem

    if output_file is None:
        output_file = '../data/' + screen_name + '.json'
    count = api.get_user(screen_name).statuses_count

    try:
        max_tweet_id = api.user_timeline(screen_name=screen_name, count=1)[0].id
    except IndexError:
        return 0

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

        tweets_json = [] 
        for tweet in tweets:
            # TODO optimise
            tweet_json = tweet_processing_json(tweet)
            if tweet_json:
                tweets_json.append(tweet_json)

        save_dict_list(tweets_json, output_file)
        print(tweets.__len__(), 'saved.')
        saved_tweet_count += tweets.__len__()
    print(screen_name, saved_tweet_count)
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

    friend_ids = api.friends_ids()
    while count > 0:
        for friend_id in friend_ids:
            try:
                friend = api.get_user(id=friend_id)
            except tweepy.error.TweepError:
                continue
            for ff_id in friend.followers_ids():
                try:
                    f_f = api.get_user(id=ff_id)
                except tweepy.error.TweepError:
                    continue
                if f_f.id in friend_ids:
                    continue
                if not f_f.protected and \
                    check_user_tweet_language(f_f.screen_name) == language and \
                    check_user_activity(f_f.screen_name) > activity:
                    f_f.follow()
                    friend_ids.append(f_f.id)
                    count -= 1
        break


def check_user_tweet_language(screen_name):
    '''
    :param screen_name: user nickname
    :return: main language of tweets
    '''
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=200)
    except tweepy.error.TweepError:
        return None
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
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=200, include_rts=False)
    except tweepy.error.TweepError:
        return 0
    if tweets.__len__() < 100 or (datetime.utcnow() - tweets[0].created_at).days > 15:
        return 0

    delta_time = (tweets[0].created_at - tweets[-1].created_at)
    delta_days = delta_time.days + delta_time.seconds / 86400 # 60*60*24
    return tweets.__len__() / delta_days


# TODO create user last readed tweet id and user id table
