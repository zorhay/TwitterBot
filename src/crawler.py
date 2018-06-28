from auth import api
from operations import *

def save_all_tweet_by_username(screen_name, output_file=None):
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
                tweet_text = get_text_from_tweet(tweet)
                urls = get_urls_from_tweet(tweet)
                tweet_text = clean_urls_from_tweet_text(tweet_text, urls)
                tweet_text = clean_usernames_from_tweet_text(tweet_text)
                f.write(tweet_text + '\n')
            print('{} saved.'.format(tweets.__len__()))
            saved_tweet_count += tweets.__len__()
    print(saved_tweet_count)
    return saved_tweet_count