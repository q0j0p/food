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
BASE_URL = 'http://allrecipes.com'
MOGODB_NAME = "allrecipes"
MONGODB_URI = 'mongodb://localhost:27017/'

class scraper(object):
    """
    Simple scraper, namely for recipes using either selenium or PhantomJS
    """
    def __init__(self, base_url, dbname = MOGODB_NAME):

        self.base_url = base_url
        try:
            self.mongoclient = pymongo.MongoClient(MONGODB_URI)
            print "Connected to {}".format(MONGODB_URI)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s".format(e)
        self.mongodbase = self.mongoclient[dbname]
        self.members_coll = self.mongodbase['members'] # Does this work?
        self.browser = "Firefox"

    def get_community_members(self, num_pages=None, browser = "Firefox", url_path = "/ask-the-community"):
        """
        Access community page using selenium and scrape, scroll down and click.
        Store entire page in database.

        Parameters
        ----------
        num_pages: int
            Number of pages ("more" button clicks).
        browser: object
            Selenium browser to use.
        url_path: string
            partial path to target page.

        Returns
        -------
        self.community_page: pymongo.collection.Collection

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
#            self.mongodbase['community_page']
        return self.community_page

    def get_community_members_continue(self, num_pages):

        for i in range(num_pages):
            self.driver.find_element_by_css_selector(
            'a.load-more-button.button.button-wide').click()
            print "clicked {} times\n".format(i)
            time.sleep(10 + random.random() * 4)
            #update page
            self.community_page = self.driver.page_source
        self.driver.close()
        return self.community_page

    def get_member_pages(self, memberid):
        """Given member ID, get all pertinent pages of member and insert into database.

        Parameters
        ----------
        memberid : string
            Allrecipe "cook" ID

        Returns
        -------
        None
        """
        base_url = self.base_url + "/cook/" + str(memberid)
        self.use_firefox()

        url = base_url + "/about-me/"
        print "accessing {} \n".format(url)
        self.driver.get(url)
        aboutme_page = self.driver.page_source

        url = base_url + "/favorites/"
        print "accessing {} \n".format(url)
        self.driver.get(url)
        favorites_page = self.driver.page_source

        url = base_url + "/following/"
        print "accessing {} \n".format(url)
        self.driver.get(url)
        following_page = self.driver.page_source

        url = base_url + "/followers/"
        print "accessing {} \n".format(url)
        self.driver.get(url)
        followers_page = self.driver.page_source

        url = base_url + "/reviews/"
        print "accessing {} \n".format(url)
        self.driver.get(url)
        reviews_page = self.driver.page_source

        url = base_url + "/made-it/"
        print "accessing {} \n".format(url)
        self.driver.get(url)
        madeit_page = self.driver.page_source

        url = base_url + "/recipes/"
        print "accessing {} \n".format(url)
        self.driver.get(url)
        recipes_page = self.driver.page_source

        client = pymongo.MongoClient(MONGODB_URI)
        members_coll = client.allrecipes.members
        members_coll.update_one(
            {"member_ID" : memberid},
            {"$set" :
                {"aboutme_page": aboutme_page,
                "favorites_page": favorites_page,
                 "following_page": following_page,
                 "followers_page": followers_page,
                 "reviews_page": reviews_page,
                 "madeit_page": madeit_page,
                 "recipes_page": recipes_page
                 "link": base_url
                }},
             upsert = True)

#        Must access database directly-- cannot acces via instance attribute 
#        return list(self.members_coll.find_one({"member_ID" : memberid},["member_ID"]))
#        return self.mongodbase['members'].find({"member_ID": memberid})


# for i,member in mems[191:]:
#     browser.get(member['link'] + "/favorites/")
#     print "list item number {}, {}\n".format(i, member['link'])
#     favorites_page = browser.page_source
#     browser.get(member['link'] + "/made-it/")
#     madeit_page = browser.page_source
#     browser.get(member['link'] + '/reviews/')
#     reviews_page = browser.page_source
#     browser.get(member['link'] + '/recipes/')
#     recipes_page = browser.page_source
#     browser.get(member['link'] + '/followers/')
#     followers_page = browser.page_source
#     browser.get(member['link'] + '/following/')
#     following_page = browser.page_source
#     db.members.update({"member_ID" : member['member_ID']},
#                    {'$set': {'favorites_page': favorites_page,
#                              'madeit_page' : madeit_page,
#                              'reviews_page' : reviews_page,
#                              'recipes_page' : recipes_page,
#                              'followers_page' : followers_page,
#                              'following_page' : following_page
#                   }})
#
#     time.sleep(5 + random.random() * 5)



    def get_page_from_list(self, urllist, collname, offset=0):
       """Given a list of urls, store page content in database

       Parameters
       ----------
       urllist : list
           List of urls.
       offset : int
           in case of interruption, start from offset index
       collname : str
           name of collection

       Returns
       -------
       None

       """

       for i,link in enumerate(urllist[offset:]):
            self.driver.get(link)
            print "list item number {}, {}\n".format(i+offset,link)
            page = self.driver.page_source
            self.mongodbase[collname].insert_one({'link': link,
                                  'page': page})
            time.sleep(5 + random.random() * 5)


    def populate_members(self, coll, ):
        """
        Given a member_ID, populate document of member (favirites,
        madeit, reviews, recipes, followers, following)
        """
        pass


    def check_dbase():
        """
        Check database stats
        """

        print self.mongodbase


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

        coll = self.mongodbase['members']
        pass


def get_recipe_ids(self):
    """Get recipe ids from recipe links in page.

    Parameters
    ----------

    """
    pass

'''
db = client.allrecipes
db.members.insert({"member_ID" : str member_ID,
                   "link" : str link,
                   "faviorites" : list favorite,
                   "madeit" : list made_it,
                   "reviews" : list reviews,
                   "personals" : list personal_recs,
                   "followers" : list followers,
                   "following" : list following,
                   "contacted" : list contacted,
                   "update_time": str update})
'''
