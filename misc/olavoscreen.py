# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.set_window_size(325, 500) # set the window size that you need 
driver.get('olavotweet.html')

sleep(2)

driver.save_screenshot('olavo1.png')

# test comment git commit
