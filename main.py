import tweepy
import yaml
import olavo


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.id_str
        keyword = ['a']
        if olavo.check_for_keyword(status.text, keywords=keyword) and 'retweeted_status' not in status.entities:
            olavo.screenshot_tweet(status.id_str)
            status_text = '{} disse "{}"!'.format(status.author.name, keyword[0])
            image_name = 'screenshot_{}.png'.format(status.id_str)
            olavo.publish_tweet(API, status=status_text, image=image_name)
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


def start_listener(api, username):
    l = MyStreamListener()
    streamer = tweepy.Stream(auth=api.auth, listener=l)
    streamer.filter(follow=[username], async=True)


if __name__ == '__main__':
    API = start_api()
    start_listener(API, '46822091')
    # tweet, filename = olavo.keyword_anniversary('odecarvalho.json')
    # olavo.publish_tweet(API, tweet, filename)
