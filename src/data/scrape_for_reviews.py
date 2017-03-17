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
import matplotlib.pyplot as plt
BASE_URL = 'http://dish.allrecipes.com'


class scraper(object):
    """
    Simple scraper, namely for recipes using either selenium or PhantomJS
    """
    def __init__(self, base_url, name='AllRecipes'):
        self.base_url = base_url
        self.name = name

    def get_community_members(self, num_pages=150):
        """
        Access community page
        Code to scroll down and click
        """
        url = self.base_url
        driver.get(url)

        pass

    def get_html(self, browser="firefox"):
        """
        """
        pass

    def use_firefox(self):
        driver = webdriver.Firefox(firefox_binary=FirefoxBinary(
        firefox_path='/Applications/FirefoxESR.app/Contents/MacOS/firefox'))

        firefox_browser.quit()


    def use_phantom(self):
        driver = webdriver.PhantomJS()
