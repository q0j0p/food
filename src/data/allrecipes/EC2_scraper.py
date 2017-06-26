'''
Scraper for EC2 websites using PhantomJS
'''
import time
from urllib import urlencode
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup as BS
import random
import requests
import pymongo
import matplotlib.pyplot as plt
import collections

N = 1  # directory is "recipe{}".format(str(N)) for recipes N * 1000 to N * 1000 + 1000
BASE_URL = "http://allrecipes.com"


# Access s3 bucket to use
AWS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET = os.environ['AWS_SECRET_ACCESS_KEY']

# Open s3 session with boto3
session = boto3.Session(aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
s3 = session.resource('s3')

mybucket = s3.Bucket('ohailolcat')

recipes_orderedset = pickle.load(open('recipes_orderedset.pkl', 'rb'))

# Configure phantomJS browser with useragent

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36/"
)

browser = webdriver.PhantomJS(desired_capabilities=dcap)
browser.implicitly_wait(2)

offset = n * 1000

for i, a in enumerate(recipes_orderedset.keys()[offset:offset+1000]):
    browser.get("http://allrecipes.com/recipe/{}/".format(a))
    print "list item number {}, {} \n  {}\n\n\n".format(i+offset, a, browser.current_url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight/1.2);")
    time.sleep(2 + random.random() * 5)
    browser.save_screenshot('recipe_{}.png'.format(a))
    mybucket.upload_file('recipe_{}.png'.format(a), 'recipes{}/recipe_{}.png'.format(str(N),a))
    with open("recipe_{}.pkl".format(a), 'wb') as f: pickle.dump(browser.page_source, f)
    mybucket.upload_file('recipe_{}.pkl'.format(a), 'recipes{}/recipe_{}.pkl'.format(str(N),a))

browser.close()
