import tweepy
import os
from olavo import screenshot_tweet, retrieve_all_tweets


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.id_str
        screenshot_tweet(status.id_str)

    def on_error(self, status_code):
        print status_code


def start_api():
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api



def start_listener(API, userId_str):
    l = MyStreamListener()
    streamer = tweepy.Stream(auth=API.auth, listener=l)
    streamer.filter(follow=[userId_str], async=True)

if __name__ == '__main__':

    API = start_api()
    # start_listener(API, '575930104')
    retrieve_all_tweets(API, '46822091')
