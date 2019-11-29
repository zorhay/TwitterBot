from datetime import datetime
from tweepy.error import TweepError
from .operations import jsonify_tweet, textify_tweet
from .helpers import save_dict_list


class TweetScraper(object):
    def __init__(self, api, scraped_ids_file=None):
        self.scraped_ids_file = scraped_ids_file or '../other/scrap_ids.txt'
        self.api = api

    def run(self, save_in_json=True):
        """
        Saves all tweets of users to whom are following.
        :param save_in_json: save tweet in json format?
        :return:
        """
        user_ids = self.api.friends_ids()
        with open(self.scraped_ids_file, 'r') as f:
            scraped_ids = f.readlines()
        scraped_ids = [int(i.strip('\n')) for i in scraped_ids]

        for user_id in list(set(user_ids) - set(scraped_ids)):
            try:
                user = self.api.get_user(id=user_id)
            except TweepError:
                continue
            screen_name, saved_tweet_count = self.save_all_tweets_by_username(user.screen_name, save_in_json)
            print(screen_name, saved_tweet_count)
            with open(self.scraped_ids_file, 'a') as f:
                f.write(user.id_str + '\n')

    def save_all_tweets_by_username(self, screen_name, in_json=True):
        """
        :param screen_name: user nickname
        :param in_json: save tweet in json format?
        :return: screen name and saved tweet count
        """

        # TODO solve limit problem

        output_file = '../data/' + screen_name + '.json' if in_json else '../data/' + screen_name + '.txt'
        count = self.api.get_user(screen_name).statuses_count
        try:
            max_tweet_id = self.api.user_timeline(screen_name=screen_name, count=1)[0].id
        except IndexError:
            return screen_name, 0

        saved_tweet_count = 0
        while count > 0:
            tweets = self.api.user_timeline(screen_name=screen_name, count=count, max_id=max_tweet_id)
            if len(tweets) <= 0 or tweets.max_id is None:
                break

            count -= len(tweets)
            max_tweet_id = tweets.max_id

            if in_json:
                tweets_json = [tweet_json for tweet_json in (jsonify_tweet(tweet)
                                                             for tweet in tweets) if tweet_json]
                save_dict_list(tweets_json, output_file)
            else:
                with open(output_file, 'a') as f:
                    f.writelines([textify_tweet(tweet) for tweet in tweets])

            print('{} saved.'.format(len(tweets)))
            saved_tweet_count += len(tweets)
        return screen_name, saved_tweet_count

    def user_scraper(self, language='hy', activity=0.25, count=100):
        """
        Follow user by activity and tweet language.
        :param language: main tweets language
        :param activity: tweets middle consistency (tweet/day)
        :param count: user max count
        :return:
        """

        # [tweet for tweet in tweepy.Cursor(api.user_timeline, screen_name=name).items()]
        # TODO solve limit problem

        friend_ids = self.api.friends_ids()
        while count > 0:
            for friend_id in friend_ids:
                try:
                    friend = self.api.get_user(id=friend_id)
                except TweepError:
                    continue
                for ff_id in friend.followers_ids():
                    try:
                        f_f = self.api.get_user(id=ff_id)
                    except TweepError:
                        continue
                    if f_f.id in friend_ids:
                        continue
                    if not f_f.protected and \
                            self._get_user_tweets_language(f_f.screen_name) == language and \
                            self._get_user_activity(f_f.screen_name) > activity:
                        f_f.follow()
                        friend_ids.append(f_f.id)
                        count -= 1
            break

    def _get_user_tweets_language(self, screen_name):
        """
        :param screen_name: user nickname
        :return: main language of tweets
        """

        try:
            tweets = self.api.user_timeline(screen_name=screen_name, count=200)
        except TweepError:
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

    def _get_user_activity(self, screen_name):
        """
        :param screen_name: user nickname
        :return: tweets middle consistency
        """

        try:
            tweets = self.api.user_timeline(screen_name=screen_name, count=200, include_rts=False)
        except TweepError:
            return 0
        if len(tweets) < 100 or (datetime.utcnow() - tweets[0].created_at).days > 15:
            return 0

        delta_time = (tweets[0].created_at - tweets[-1].created_at)
        delta_days = delta_time.days + delta_time.seconds / 86400  # 60*60*24
        return len(tweets) / delta_days

    # TODO create user last readed tweet id and user id table
