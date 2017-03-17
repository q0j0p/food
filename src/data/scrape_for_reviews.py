'''
Scrape websites using Firefox or PhantomJS
'''
import time
from urllib import urlencode  # TODO(Miles): Python 3
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import random
import requests
import pymongo
import matplotlib.pyplot as plt
BASE_URL = 'http://dish.allrecipes.com'


class scraper(object):
    """
    Simple scraper, namely for recipes using either selenium or PhantomJS
    """
    def __init__(self, base_url, dbname='allecipes', browser):
        MONGODB_PATH = 'mongodb://localhost:27017/'
        self.base_url = base_url
        self.name = name
        self.browser = browser
        try:
            self.mongoclient = pymongo.MongoClient(MONGODB_PATH)
            print "Connected to {}".format(MONGODB_PATH)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s".format(e)
        self.mongodbase = self.mongoclient[dbname]
        


    def get_community_members(self, num_pages=None, url_path = "/ask-the-community"):
        """
        Access community page
        Code to scroll down and click
        """
        # Set URL
        url = self.base_url + path
        # Load URL on browser
        self.driver.get(url)
        # In allrecipes, I need to scroll down 3 times, then click on "more" button.
        if num_pages:
            for i in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print "scroll {} times \n".format(i)
            for i in range(num_pages):
                self.browser.find_element_by_css_selector(
                'a.load-more-button.button.button-wide').click()
                print "clicked {} times\n".format(i)
                time.sleep(10 + random.random() * 4)
                #update page
                self.community_page = driver.page_source






    def get_html(self, browser="firefox"):
        """
        """
        pass

    def use_firefox(self):
        self.driver = webdriver.Firefox(firefox_binary=FirefoxBinary(
        firefox_path='/Applications/FirefoxESR.app/Contents/MacOS/firefox'))

        firefox_browser.quit()


    def use_phantom(self):
        self.driver = webdriver.PhantomJS()
