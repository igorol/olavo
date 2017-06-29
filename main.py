import tweepy
import yaml
# from apscheduler.schedulers.background import BackgroundScheduler
from olavo import screenshot_tweet, publish_tweet, check_for_keyword
from datetime import datetime


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, id_str, keyword):
        self.id_str = id_str
        self.keyword = keyword

    def on_status(self, status):
        if check_for_keyword(status.text, keyword=self.keyword) and 'retweeted_status' not in status.entities:
            screenshot_tweet(status.id_str)
            status_text = 'Olavo disse "{}"'.format(self.keyword)
            image_name = 'screenshot_{}.png'.format(status.id_str)
            publish_tweet(API, status=status_text, image=image_name)
            print 'status updated'

    def on_error(self, status_code):
        print 'Error : {}'.format(status_code)


def start_api():
    with open('info.yaml', 'r') as f:
        doc = yaml.load(f)

    consumer_key = doc['tokens']['consumer_key']
    consumer_secret = doc['tokens']['consumer_secret']
    access_token = doc['tokens']['access_token']
    access_token_secret = doc['tokens']['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def start_listener(api, user_id_str, keyword):
    """

    :param api:  Tweepy API object
    :param user_id_str: Id of user you want to 'lister'
    :param keyword: keyword you want to monitor
    :return:
    """
    l = MyStreamListener(user_id_str, keyword)
    streamer = tweepy.Stream(auth=api.auth, listener=l)
    streamer.filter(follow=[user_id_str], async=True)


if __name__ == '__main__':
    ##
    ## Start main API object
    ##
    API = start_api()

    ##
    ## Start Stream Listener
    ##
    start_listener(API, user_id_str='46822091', keyword='cu')


    ##
    ## Schedule important events
    ##
    # sched = BackgroundScheduler()
    # sched.start()
    # sched.add_job(publish_tweet, 'cron', minute='14', hour='20',
    #               args=[API, 'Test scheduled update status {}'.format(datetime.now())])

    ## Other functions

    # retrieve_all_tweets(API, '46822091')
    # status_id_str = '865178906013437954'
    # screenshot_tweet(status_id_str)
    # status_text = 'Test update status {}'.format(datetime.now())
    # image_name = 'screenshot_{}.png'.format(status_id_str)
    # publish_tweet(API, status=status_text, image=image_name)
