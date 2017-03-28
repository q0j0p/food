import time
from urllib import urlencode
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup as BS
import random
import requests
import pymongo
import pandas as pd
import re

browser = webdriver.PhantomJS()
# get the 'page' field from document

for i,member in mems[49:]:
    browser.get(member['link'] + "/favorites/")
    print "list item number {}, {}\n".format(i, member['link'])
    favorites_page = browser.page_source
    browser.get(member['link'] + "/made-it/")
    madeit_page = browser.page_source
    browser.get(member['link'] + '/reviews/')
    reviews_page = browser.page_source
    browser.get(member['link'] + '/recipes/')
    recipes_page = browser.page_source
    browser.get(member['link'] + '/followers/')
    followers_page = browser.page_source
    browser.get(member['link'] + '/following/')
    following_page = browser.page_source
    db.members.update({"member_ID" : member['member_ID']},
                   {'$set': {'favorites_page': favorites_page,
                             'madeit_page' : madeit_page,
                             'reviews_page' : reviews_page,
                             'recipes_page' : recipes_page,
                             'followers_page' : followers_page,
                             'following_page' : following_page
                  }})

    time.sleep(5 + random.random() * 5)
