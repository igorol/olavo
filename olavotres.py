# __author__ = 'igoro'

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from ConfigParser import SafeConfigParser
import simplejson
import re

parser = SafeConfigParser()
parser.read('olavo_keys.ini')

# olavodissecu credentials
consumer_key = parser.get('main','consumer_key')
consumer_secret = parser.get('main','consumer_secret')
access_token = parser.get('main','access_token')
access_token_secret = parser.get('main','access_token_secret')

# nao entendo o conceito de class. isso tem que ir dentro da class OlavoListener?
def temcu(w, keyword='cu'):
    lista_palavras = re.split('\W+', w.lower())
    return keyword in lista_palavras

#Basic Listener
class OlavoListener(StreamListener):

    def on_data(self, data):
        #print '_____'
        obj= simplejson.loads(data)
        #print obj['user']['id']
        print obj
        # print obj['text'].lower()
        # aaa = obj['user']
        # print aaa['screen_name']
        # check_for_string(obj)
        if 'user' in obj and obj['user']['id'] == 46822091: #depois fazer id flutuar, e numero
            print 'passo usuario: eh target'
            if temcu(obj['text']) or temcu(obj['text'],'cus'): #check for presence of keyword
                print 'passo temcu: achamos cu'
                tttext = 'Olavo disse cu. http://www.twitter.com/' + obj['user']['screen_name'] + '/status/' + obj['id_str']
                print tttext
                API = tweepy.API(auth)
                API.update_status(status=tttext)
                # podemos passar o original Tweet ID to the in_reply_to_status_id parameter
            else:
                print 'passo temcu: nao achamos cu'
        else:
            print 'passo usuario: nao eh target'

        return True

    def on_error(self, status):
        print 'Error :'+str(status)


if __name__ == '__main__':

    l = OlavoListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth,l)

# some users id's
# operacoesrio  : 226409689
# odecarvalho   : 46822091
# hypthreed     : 216881060
# afp           : 380648579

    stream.filter(follow=['46822091'],filter_level='low')




