from selenium import webdriver
from PIL import Image
from datetime import datetime

import unicodedata
import os
import csv
import re
import string

import pandas as pd


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str.decode("utf-8"))
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def check_for_keyword(text, keywords=['cu', 'cus']):
    keywords = [x.lower() for x in keywords]
    text = remove_accents(text.encode('utf8'))
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    stripped_text = regex.sub('', text).lower()
    word_list = re.split('\W+', stripped_text)
    # return keyword.lower() in word_list
    return any(word in word_list for word in keywords)


def publish_tweet(api, status, image=None):
    """

    :param api: API object
    :param status: String with status text
    :param image:  Filename of png to be attached to status
    :return:
    """

    if image:
        api.update_with_media(filename='./screenshots/{}'.format(image), status=status)
    else:
        api.update_status(status=status)


def screenshot_tweet(id_str):
    """

    Saves a PNG screenshot of a tweet given by id_src

    :param id_str: Id of tweet in string format
    :return:
    """
    try:
        driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 768)
        driver.get('https://twitter.com/statuses/{}?lang=pt-br'.format(id_str))

        # getting element containing the tweet body
        element = driver.find_element_by_class_name('permalink-tweet-container')
        location = element.location
        size = element.size
        driver.save_screenshot('./screenshots/full_screenshot_{}.png'.format(id_str))
        driver.quit()

        # cropping the full screenshot around desired element
        im = Image.open('./screenshots/full_screenshot_{}.png'.format(id_str))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((left, top, right, bottom))
        im.save('./screenshots/screenshot_{}.png'.format(id_str))
        os.remove('./screenshots/full_screenshot_{}.png'.format(id_str))
        return 'screenshot_{}.png'.format((id_str))
    except:
        return -1


def extract_from_corpus(corpus_file, keywords=['cu']):
    corpus_df = pd.read_json(corpus_file)
    corpus_df = corpus_df.sort_values(by=['created_at'])

    selected_indices = []

    idx = 0
    for row in corpus_df.iterrows():
        if check_for_keyword(row[1]['text'], keywords=keywords):
            selected_indices.append(idx)
        idx += 1

    new_corpus = corpus_df.iloc[selected_indices]

    return new_corpus


def keyword_anniversary(corpus_file, keywords=['cu', 'cus'], save_png=True):
    new = extract_from_corpus(corpus_file, keywords=keywords)
    tweet = -1

    for index, row in new.iterrows():
        if datetime.now().strftime('%m%d') == row['created_at'].strftime('%m%d'):
            anniversary = datetime.now().year - row['created_at'].year
            if anniversary == 1:
                yearword = 'ano'
            else:
                yearword = 'anos'

            tweet = " Tunel do tempo: ha {} {}, Olavo disse cu".format(anniversary, yearword, row['created_at'].strftime('%Y-%m-%d'))

            if save_png:
                filename = screenshot_tweet(str(row.id))
            else:
                filename = -1

            return tweet, filename


def retrieve_all_tweets(api, id_scr):
    """
    Retrieve all tweets from a specific user and saves them in a csv file

    :param api: Tweepy API object
    :param id_scr: Twitter user id, in string format
    :return:
    """
    full_tweet_list = []
    new_tweets = api.user_timeline(user_id=id_scr, count=200)
    full_tweet_list.extend(new_tweets)
    oldest = full_tweet_list[-1].id - 1

    while len(new_tweets) > 0:
        print "getting tweets before {}".format(oldest)
        new_tweets = api.user_timeline(user_id=id_scr, count=200, max_id=oldest)
        full_tweet_list.extend(new_tweets)
        oldest = full_tweet_list[-1].id - 1

    out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities] for tweet in
                  full_tweet_list]

    with open('{}_tweets.csv'.format(id_scr), 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "entities"])
        writer.writerows(out_tweets)
