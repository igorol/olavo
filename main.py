import tweepy
import os
from olavo import screenshot_tweet, publish_tweet
from datetime import datetime


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.id_str
        screenshot_tweet(status.id_str)
        status_text = 'Test update status {}'.format(datetime.now())
        image_name = 'screenshot_{}.png'.format(status.id_str)
        publish_tweet(API, status=status_text, image=image_name)
        print 'status updated'

    def on_error(self, status_code):
        print 'Error : {}'.format(status_code)


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

    ## Start main API object
    API = start_api()

    ## Start Stream Listener
    ## Warning, it will perform all the actions defined in `MyStreamListener` class
    # start_listener(API, '575930104')


    ## Other functions

    # retrieve_all_tweets(API, '46822091')
    status_id_str = '865178906013437954'
    screenshot_tweet(status_id_str)
    status_text = 'Test update status {}'.format(datetime.now())
    image_name = 'screenshot_{}.png'.format(status_id_str)
    publish_tweet(API, status=status_text, image=image_name)
