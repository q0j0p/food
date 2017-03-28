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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import matplotlib.pyplot as plt
from IPython.display import Image


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36/"
)
 browser = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])

browser = webdriver.PhantomJS(desired_capabilities=dcap)
browser.implicitly_wait(10)

with open('memlist.txt', 'r') as f:
        meml = [x for x in f.readlines() ]
memlist = [m.strip() for m in meml]

favorites_page = []

for i, member in enumerate(memlist):
    browser.get("http://allrecipes.com/cook/"+member + "/favorites/")
    print "list item number {}, {} \n  {}\n\n\n".format(i, member,browser.current_url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight/1.2);")
    time.sleep(10)
    time.sleep(5 + random.random() * 5)
    favorites_page.append(browser.page_source)
    browser.save_screenshot('screen{}.png'.format(member))
#    Image('screen{}.png'.format(member))
