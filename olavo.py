from selenium import webdriver
from PIL import Image
import os
import csv


def screenshot_tweet(id_scr):
    """

    Saves a PNG screenshot of a tweet given by id_src

    :param id_scr: Id of tweet in string format
    :return:
    """
    driver = webdriver.PhantomJS()
    # driver.set_window_size(1024, 768)
    driver.get('https://twitter.com/statuses/{}'.format(id_scr))

    # getting element containing the tweet body
    # element = driver.find_element_by_class_name('js-original-tweet')
    element = driver.find_element_by_class_name('permalink-tweet')
    print element
    location = element.location
    size = element.size
    print size
    print location
    driver.save_screenshot('full_screenshot_{}.png'.format(id_scr))
    driver.quit()

    ## cropping the full screenshot around desired element
    im = Image.open('full_screenshot_{}.png'.format(id_scr))  # uses PIL library to open image in memory
    left = location['x'] + 10
    top = location['y']
    right = location['x'] + size['width'] + 120
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save('screenshot_{}.png'.format(id_scr))
    ## os.remove('full_screenshot_{}.png'.format(id_scr))


def retrieve_all_tweets(api, id_scr):
    """
    Retrieve all tweets from a specific user and saves them in a csv file

    :param api: Tweepy API object
    :param id_scr: Twitter user id, in string format
    :return:
    """
    alltweets = []
    new_tweets = api.user_timeline(user_id=id_scr, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print "getting tweets before {}".format(oldest)
        new_tweets = api.user_timeline(user_id=id_scr, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

    out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    with open('{}_tweets.csv'.format(id_scr), 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(out_tweets)
