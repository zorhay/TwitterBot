import tweepy
import auth

auth.authentication()

for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
    print ("Followed everyone that is following " + user.name)