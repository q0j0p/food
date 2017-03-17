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
    def __init__(self, base_url, dbname='allecipes'):
        MONGODB_URI = 'mongodb://localhost:27017/'
        self.base_url = base_url
        self.name = dbname
        try:
            self.mongoclient = pymongo.MongoClient(MONGODB_URI)
            print "Connected to {}".format(MONGODB_URI)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s".format(e)
        self.mongodbase = self.mongoclient[dbname]



    def get_community_members(self, num_pages=None, browser = "Firefox", url_path = "/ask-the-community"):
        """
        Access community page
        Code to scroll down and click
        """
        # Set URL
        url = self.base_url + url_path
        if browser == "Firefox":
            self.use_firefox()
        # Load URL on browser
        self.driver.get(url)
        # In allrecipes, I need to scroll down 3 times, then click on "more" button.
        if num_pages:
            for i in range(4):
                time.sleep(9+random.random() * 2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.2);")
                print "scroll {} times \n".format(i)
            for i in range(num_pages):
                self.driver.find_element_by_css_selector(
                'a.load-more-button.button.button-wide').click()
                print "clicked {} times\n".format(i)
                time.sleep(10 + random.random() * 4)
                #update page
                self.community_page = self.driver.page_source
        return self.community_page

    def get_community_members_continue(self, num_pages):
        for i in range(num_pages):
            self.driver.find_element_by_css_selector(
            'a.load-more-button.button.button-wide').click()
            print "clicked {} times\n".format(i)
            time.sleep(10 + random.random() * 4)
            #update page
            self.community_page = self.driver.page_source
        return self.community_page




    def get_html(self, browser="firefox"):
        """
        """
        pass

    def use_firefox(self):
        self.driver = webdriver.Firefox(firefox_binary=FirefoxBinary(
        firefox_path='/Applications/FirefoxESR.app/Contents/MacOS/firefox'))

        #firefox_browser.quit()


    def use_phantom(self):
        self.driver = webdriver.PhantomJS()
