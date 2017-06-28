from selenium import webdriver
from PIL import Image
import os
import csv
import re


def check_for_keyword(w, keyword='cu'):
    word_list = re.split('\W+', w.lower())
    return keyword in word_list

def publish_tweet(api, status, image = None):
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
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)
    driver.get('https://twitter.com/statuses/{}?lang=pt-br'.format(id_str))

    # getting element containing the tweet body
    element = driver.find_element_by_class_name('permalink-tweet-container')
    location = element.location
    size = element.size
    driver.save_screenshot('./screenshots/full_screenshot_{}.png'.format(id_str))
    driver.quit()

    ## cropping the full screenshot around desired element
    im = Image.open('./screenshots/full_screenshot_{}.png'.format(id_str))  # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save('./screenshots/screenshot_{}.png'.format(id_str))
    os.remove('./screenshots/full_screenshot_{}.png'.format(id_str))





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

    out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities] for tweet in full_tweet_list]

    with open('{}_tweets.csv'.format(id_scr), 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "entities"])
        writer.writerows(out_tweets)
