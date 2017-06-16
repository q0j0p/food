'''
Scrape websites using Firefox or PhantomJS
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
import os
import boto3
import pickle

AWS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET = os.environ['AWS_SECRET_ACCESS_KEY']

BASE_URL = 'http://allrecipes.com'
MOGODB_NAME = "allrecipes"
MONGODB_URI = 'mongodb://localhost:27017/'

class Scraper(object):
    """
    Simple scraper for the allrecipes.com website.

    Methods
    -------


    """
    def __init__(self, base_url=BASE_URL, dbname = MOGODB_NAME, browser= "Firefox"):

        self.base_url = base_url
        try:
            self.mongoclient = pymongo.MongoClient(MONGODB_URI)
            print "Connected to {}".format(MONGODB_URI)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s".format(e)
        self.mongodbase = self.mongoclient[dbname]
        self.members_coll = self.mongodbase['members']
        self.recipes_coll = self.mongodbase['recipes']
        self.browser = browser
        if self.browser == "Firefox":
            self.use_firefox()
        elif self.browser == "Phantom":
            self.use_phantom()

    def get_community_page_scrolled(self,
            num_pages=None,
            browser = "Firefox",
            url_path = "/recipes/84/healthy-recipes/"):
        """Access community page using selenium and scrape, scroll down and click.
        Store entire page in database.

        Parameters
        ----------
        num_pages: int
            Number of pages (number of "more" button clicks).
        browser: object
            Selenium browser to use ("Firefox" ).
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
            for i in range(5):
                time.sleep(9+random.random() * 2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print "scroll {} times \n".format(i)
            for i in range(num_pages):
                self.driver.find_element_by_css_selector(
                    'button.btns-one-small').click()
                print "clicked {} times\n".format(i)
                time.sleep(5 + random.random() * 4)
                for i in range(5):
                    time.sleep(5+random.random() * 2)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print "scroll {} times \n".format(i)
                    time.sleep(5 + random.random() * 4)
                #update page
                self.community_page = self.driver.page_source
#            self.mongodbase['community_page']
        return self.driver.page_source

    def get_community_members(self, num_pages=None,
      browser = "Firefox",
      url_path = "/ask-the-community"):
        """
        Access community page using selenium and scrape, scroll down and click.
        Store entire page in database, but also return page as text.

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
            HTML text of a single web page, continuously scrolled down `num_pages` times.
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
                time.sleep(9+random.random() * 2) # randomized pause times
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.2);")
                print "scroll {} times \n".format(i)
            for i in range(num_pages):
                self.driver.find_element_by_css_selector(
                    'a.load-more-button.button.button-wide').click()  #emulate button click on brower
                print "clicked {} times\n".format(i)
                time.sleep(10 + random.random() * 4)
                #update saved page
                self.community_page = self.driver.page_source
#            self.mongodbase['community_page']
        return self.community_page #return as variable too

    def get_community_members_continue(self, num_pages):
        """Continue on from previous iteration of community page acquisition"""
        for i in range(num_pages):
            self.driver.find_element_by_css_selector(
            'a.load-more-button.button.button-wide').click()
            print "clicked {} times\n".format(i)
            time.sleep(10 + random.random() * 4)
            #update page
            self.community_page = self.driver.page_source
        self.driver.close()
        return self.community_page

    def check_member_records(self, member_ID):
        """Check for completeness of member_ID's records"""
        member_list = list(self.members_coll.find({"member_ID":member_ID}))
        if len(member_list) != 1:
            print "Error: Number of documents (mongodb) for {} is {}.".format(member_ID, len(member_list))
        else:
            record = member_list[0]
        if record.get('followers_dict'):
            followers = len(record.get('followers_dict'))
        else:
            followers = None
        if record.get('following_dict'):
            following = len(record.get('following_dict'))
        else:
            following = None
        if record.get('reviews_dict'):
            reviews = len(record.get('reviews_dict'))
        else:
            reviews = None
        if record.get('favorites_dict'):
            favorites = len(record.get('favorites_dict'))
        else:
            favorites = None
        if record.get('madeits_dict'):
            madeits = len(record.get('madeits_dict'))
        else:
            madeits = None

        print """
             member_ID is {}
             has "about me" page: {}
             number of followers: {}
             number of followed: {}
             number of reviews: {}
             number of favorites: {}
             number of recipes made: {}
             """.format(record['member_ID'],
                        bool(record['aboutme']),
                        followers,
                        following,
                        reviews,
                        favorites,
                        madeits
                        )

    def get_member_pages(self, memberid):
        """Given member ID, get all pertinent pages directly from member webpage
        and insert into member's MongoDB document.

        Parameters
        ----------
        memberid : string
            Allrecipe "cook" ID

        Returns
        -------
        members_coll
        """
        base_url = self.base_url + "/cook/" + str(memberid)
#        self.use_firefox()

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
        member_pages_coll = client.allrecipes.member_pages
        member_pages_coll.update_one(
            {"member_ID" : memberid},
            {"$set" :
                {"aboutme_page": aboutme_page,
                "favorites_page": favorites_page,
                 "following_page": following_page,
                 "followers_page": followers_page,
                 "reviews_page": reviews_page,
                 "madeit_page": madeit_page,
                 "recipes_page": recipes_page,
                 "link": base_url
                }},
             upsert = True)

        return member_pages_coll

    def get_members_reviews(self):
        """Populate member's 'review' data in 'allrecipes.members' collection by processing
        review page.

        Parameters
        ----------

        """

        client = pymongo.MongoClient(MONGODB_URI)
        members_coll = client.allrecipes.members

        noreviews_docs_cursor = self.members_coll.find(
            {"member_ID": {"$exists":True},
                "reviews": {"$exists": False}},
                ["member_ID", "reviews_page"]
                )
        print "Count of member documents with no reviews field:", \
            noreviews_docs_cursor.count()

        print "docs processed:"
        for doc in noreviews_docs_cursor:
            doc_reviews_data = self._get_reviews_data(doc['reviews_page'])
            members_coll.find_one_and_update({"member_ID": doc['member_ID']},
                {"$set": {"reviews_recipe_id_list": doc_reviews_data[0],
                          "reviews_dict": doc_reviews_data[1]}},
                          upsert = True)
            print doc['member_ID']

        noreviews_docs_cursor = self.members_coll.find(
            {"member_ID": {"$exists":True},
                "reviews": {"$exists": False}},["member_ID"])
        print "Count of member documents with no reviews field:",\
            noreviews_docs_cursor.count()


    def _get_reviews_data(self, page):

            soup = BS(page, "html.parser")

            # Extract pertinent info from soup
            reviews_rating_list = [a.attrs['data-rating'] \
                for a in soup.select("article.profile-review-card div.rated-review--stars div.ng-isolate-scope")]
            reviews_recipe_id_list = [a.attrs['data-ng-href'].split('/')[2] \
                for a in soup.select("article.profile-review-card div.rated-review--stars a.ng-scope")]
            reviews_recipe_links_list = [a.attrs['data-ng-href'] \
                for a in soup.select("article.profile-review-card div.rated-review--stars a.ng-scope")]
            reviews_recipe_title_list = [a.text
                for a in soup.select("article.profile-review-card h3.ng-binding")]
            reviews_text_list = [a.text
                for a in soup.select("article.profile-review-card div.rated-review-text")]

            reviews = zip(reviews_recipe_id_list, reviews_recipe_title_list, reviews_rating_list,
                           reviews_recipe_links_list, reviews_text_list)
            # For each review, create a dict w/ keys= ['recipe_ID', 'recipe_title', 'recipe_rating', 'recipe_link', 'review_text']
            reviews_dict_list = [dict(zip(['recipe_ID', 'recipe_title', 'recipe_rating',
                                           'recipe_link', 'review_text'], a)) for a in reviews]
            return (reviews_recipe_id_list, reviews_dict_list)


    def get_members_madeits(self):
        """Get member's 'made it' info"""

        client = pymongo.MongoClient(MONGODB_URI)
        members_coll = client.allrecipes.members

        no_madeitlist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "madeits_dict": {"$exists": False}}, ["member_ID", "madeit_page"])
        print "Count of member documents with no madeit field:", no_madeitlist_docs_cursor.count()

        has_madeitlist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "madeits_dict": {"$exists": True}}, ["member_ID", "madeit_page"])
        print "Count of member documents with madeit field:", has_madeitlist_docs_cursor.count()

        print "docs processed:"
        for doc in no_madeitlist_docs_cursor:
            doc_madeits_data = self._get_madeits_data(doc['madeit_page'])
            members_coll.find_one_and_update({"member_ID": doc['member_ID']},
                {"$set": {"madeits_recipe_id_list": doc_madeits_data[0],
                          "madeits_dict": doc_madeits_data[1]}},
                          upsert = True)
            print doc['member_ID']
        no_madeitlist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "madeits_dict": {"$exists": False}},["member_ID"])
        print "Count of member documents with no madeits field:", no_madeitlist_docs_cursor.count()


    def _get_madeits_data(self, page):
        """Extract 'made it' information from page"""

        soup = BS(page, "html.parser")

        # Extract pertinent info from soup
        madeit_names_list = [a.text.replace(".","") for a in collections.OrderedDict.fromkeys(soup.select('article.grid-col--fixed-tiles div.ng-scope h3.grid-col__h3--recipe-grid a.ng-scope')) if a.text != ' ']
        madeit_recipe_ID_list = [a.split('/')[2] for a in collections.OrderedDict.fromkeys([a.attrs['data-ng-href'] for a in soup.select('article.grid-col--fixed-tiles div.ng-scope h3.grid-col__h3--recipe-grid a.ng-scope')])]
        madeit_list_dict = dict(zip(madeit_names_list, madeit_recipe_ID_list))

#        Must access database directly-- cannot acces via instance attribute
#        return list(self.members_coll.find_one({"member_ID" : memberid},["member_ID"]))
#        return self.mongodbase['members'].find({"member_ID": memberid})
        return (madeit_recipe_ID_list, madeit_list_dict)


    def get_members_favorites(self):
        """Get member's 'made it' info"""

        # client = pymongo.MongoClient(MONGODB_URI)
        # members_coll = client.allrecipes.members

        no_favoriteslist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "favorites_dict": {"$exists": False}}, ["member_ID", "favorites_page"])
        print "Count of member documents with no favorites field:", no_favoriteslist_docs_cursor.count()

        has_favoriteslist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "favorites_dict": {"$exists": True}}, ["member_ID", "favorites_page"])
        print "Count of member documents with favorites field:", has_favoriteslist_docs_cursor.count()

        print "docs processed:"
        for doc in no_favoriteslist_docs_cursor:
            doc_favorites_data = self._get_favorites_data(doc['favorites_page'])
            self.members_coll.find_one_and_update({"member_ID": doc['member_ID']},
                {"$set": {"favorites_recipe_id_list": doc_favorites_data[0],
                          "favorites_dict": doc_favorites_data[1]}},
                          upsert = True)
            print doc['member_ID']
        no_favoriteslist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "favorites_dict": {"$exists": False}},["member_ID"])
        print "Count of member documents with no favorites field:", no_favoriteslist_docs_cursor.count()


    def _get_favorites_data(self, page):

        soup = BS(page, "html.parser")

        # Extract pertinent info from soup, zip up to make dict.
        favorites_id_list = [a['href'].split('/')[2] for a in collections.OrderedDict.fromkeys(soup.select("h3.grid-col__h3 a.ng-scope"))]
        favorites_name_list = [a.attrs['href'].split('/')[3] for a in collections.OrderedDict.fromkeys(soup.select("h3.grid-col__h3 a.ng-scope"))]
        favorites_recipe_dict = dict(zip(favorites_name_list, favorites_id_list))
        return (favorites_id_list, favorites_recipe_dict)


    def get_members_following(self):
        """Get the ID and names of people followed by the members"""
        no_followinglist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "following_dict": {"$exists": False}}, ["member_ID", "following_page"])
        print "Count of member documents with no following field:", no_followinglist_docs_cursor.count()

        has_followinglist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "following_dict": {"$exists": True}}, ["member_ID", "following_page"])
        print "Count of member documents with following field:", has_followinglist_docs_cursor.count()

        print "docs processed:"
        for doc in no_followinglist_docs_cursor:
            doc_following_data = self._get_following_data(doc['following_page'])
            self.members_coll.find_one_and_update({"member_ID": doc['member_ID']},
                {"$set": {"following_recipe_id_list": doc_following_data[0],
                          "following_dict": doc_following_data[1]}},
                          upsert = True)
            print doc['member_ID']
        no_followinglist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "following_dict": {"$exists": False}},["member_ID"])
        print "Count of member documents with no following field:", no_followinglist_docs_cursor.count()


    def _get_following_data(self, page):

        soup = BS(page, "html.parser")

        following_id_list = [a.attrs['data-ng-href'].split('/')[2] for a in collections.OrderedDict.fromkeys(soup.select('article.grid-col a.ng-scope')) if a.text != ' ']
        following_names_list = [a.text.strip().replace(".","") for a in collections.OrderedDict.fromkeys(soup.select('article.grid-col a.ng-scope')) if a.text != ' ']
        following_dict = dict(zip(following_names_list, following_id_list))

        return (following_id_list, following_dict)


    def get_members_followers(self):
        """Get the ID and names of people followed by the members"""
        no_followerslist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "followers_dict": {"$exists": False}}, ["member_ID", "followers_page"])
        print "Count of member documents with no followers field:", no_followerslist_docs_cursor.count()

        has_followerslist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "followers_dict": {"$exists": True}}, ["member_ID", "followers_page"])
        print "Count of member documents with followers field:", has_followerslist_docs_cursor.count()

        print "docs processed:"
        for doc in no_followerslist_docs_cursor:
            doc_followers_data = self._get_followers_data(doc['followers_page'])
            self.members_coll.find_one_and_update({"member_ID": doc['member_ID']},
                {"$set": {"followers_recipe_id_list": doc_followers_data[0],
                          "followers_dict": doc_followers_data[1]}},
                          upsert = True)
            print doc['member_ID']
        no_followerslist_docs_cursor = self.members_coll.find({"member_ID": {"$exists":True},
                                                        "followers_dict": {"$exists": False}},["member_ID"])
        print "Count of member documents with no followers field:", no_followerslist_docs_cursor.count()


    def _get_followers_data(self, page):

        soup = BS(page, "html.parser")

        followers_id_list = [a.attrs['data-ng-href'].split('/')[2] for a in collections.OrderedDict.fromkeys(soup.select('article.grid-col a.ng-scope')) if a.text != ' ']
        followers_names_list = [a.text.strip().replace(".","") for a in collections.OrderedDict.fromkeys(soup.select('article.grid-col a.ng-scope')) if a.text != ' ']
        followers_dict = dict(zip(followers_names_list, followers_id_list))

        return (followers_id_list, followers_dict)


    def get_members_aboutme_from_pkl(self, filename):
        """Get pertinent info from members' 'about me' section.  This section
        was scraped and pickled separate from the other sections.

        ** used ad hoc notebook for initial scrape**
        Parameters
        ----------
        filename: str
            pickle file of list of 'about me' pages
        """
        pages_list = pickle.load(open('filename', 'rb'))

        for page in pages_list:
            member_id, aboutme_text = self._get_aboutme_data(page)
            members_coll.find_one_and_update({"member_ID": member_id},
                                    {"$set": {"aboutme": aboutme_text}},
                                    upsert = True)

        print "members with about me page:",members_coll.find({"aboutme": {"$exists": True}}).count()
        print "members without about me page:",members_coll.find({"aboutme": {"$exists": False}}).count()


    def _get_aboutme_data(self, page):
        """Given page, extract member_ID and 'about me' text.
        """
        soup = BS(page, "html.parser")
        text = [a.text for a in soup.select('li.about-me--description.ng-binding')]
        id = [a.attrs['href'].split('/')[2] \
            for a in soup.select('div.profile-shell.full-page.ng-scope a.btns-two-small')][0]
        return (id, text)

    def get_recipe_pkl_page_from_aws(self, s3key):

        session = boto3.Session(aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
        s3 = session.resource('s3')
        mybucket = s3.Bucket('ohailolcat')
        for f in mybucket.objects.filter(Prefix='{}/'.format(s3key)):
            fn = f.key.split('/')[1]
            if (fn.startswith('recipe_')) & (fn[-4:] == ".pkl"):
                recipe_ID = fn.split(".")[0][7:]
                self.recipes_coll.find_one_and_replace({"recipe_ID": recipe_ID},
                                      {"$set": {"page": pickle.loads(f.get()['Body'].read())}},
                                      upsert = True)
                print "recipe {} added".format(recipe_ID)
        print "recipes with page:",self.recipes_coll.find({"page": {"$exists": True}}).count()
        print "recipes without page:",self.recipes_coll.find({"page": {"$exists": False}}).count()


    def get_recipe_data(self):
        no_recipedata_docs_cursor = self.recipes_coll.find({"recipe_ID": {"$exists":True},
                                                    "name": {"$exists": False}},
                                                    ["recipe_ID", "page"],
                                                    modifiers= {"$snapshot":True})
        print "Count of recipe documents with no recipe data:", no_recipedata_docs_cursor.count()

        has_recipedata_docs_cursor = self.members_coll.find({"recipe_ID": {"$exists":True},
                                                    "name": {"$exists": True}},
                                                    ["recipe_ID", "page"],
                                                    modifiers = {"$snapshot":True})
        print "Count of recipe documents with no recipe data:", has_recipedata_docs_cursor.count()

        for doc in no_recipedata_docs_cursor:
            doc_recipe_data = self._get_recipe_data(doc['page'])
            self.recipes_coll.find_one_and_update({"recipe_ID": doc['recipe_ID']},
                {"$set": {"name": doc_recipe_data[0],
                          "description": doc_recipe_data[1],
                          "ingredients_list": doc_recipe_data[2],
                          "recipe_times": doc_recipe_data[3],
                          "directions_list": doc_recipe_data[4],
                          "servings": doc_recipe_data[5],
                          "rating_list": doc_recipe_data[6],
                          "servings_config": doc_recipe_data[7],
                          "nutrition_serving_info": doc_recipe_data[8],
                          "nutrition_info": doc_recipe_data[9],
                          "nutrition_elements": doc_recipe_data[10]}},
                          upsert = True)
            print doc['recipe_ID']
        no_recipedata_docs_cursor = self.recipes_coll.find({"recipe_ID": {"$exists":True},
                                                        "name": {"$exists": False}},["recipe_ID"])
        print "Count of member documents with no recipe name field:", no_recipedata_docs_cursor.count()


    def _get_recipe_data(self, page):
        """Given html document of a recipe, parse and output relevant fields.

        Parameters
        ----------
        page : obj
            html document of recipe

        Returns
        -------
        [Tuple of strings corresponding to recipe data, all strings]
        recipe_name : [0]
        description : [1]
        ingredients_list : [2]
        recipe_times : [3]
        directions_list : [4]
        servings : [5]
        rating_list : [6]
        servings_config : [7]
        nutrition_servings_info : [8]
        nutrition_info : [9]
        nutrition_elements : [10]
        """

        s = BS(page, "html.parser")

        recipe_name = [a.text for a in s.select("h1.recipe-summary__h1")]
        description = [a.text.strip() for a in s.select("div.submitter__description")]
        ingredients_list = [a.text \
            for a in s.select("span.recipe-ingred_txt")][:-1]
        times = [a.attrs['datetime'] \
            for a in s.select("div.directions--section time")]
        directions_list = [a.text.strip() \
            for a in s.select("ol.list-numbers.recipe-directions__list li.step")]
        servings = [a.text for a in s.select("span.servings-count")]
        rating_list = [a.attrs['content'] \
            for a in s.select("section.recipe-summary.clearfix meta")]
        servings_config = [a.text.strip() \
            for a in s.select("section.recipe-ingredients.ng-scope")]
        nutrition_servings_info = [a.text.strip().split("\n") \
            for a in s.select("div.fullNutrition div.top.light-underline")]
        nutrition_info = "".join([a.text \
            for a in s.select("div.recipe-nutrition__form li")]).split('\n')
        nutrition_elements = [a.attrs['nutrient'] \
            for a in s.select('li.light-underline div')]
        return (recipe_name, description, ingredients_list, times, directions_list,
                servings, rating_list,
                servings_config, nutrition_servings_info, nutrition_info, nutrition_elements)


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
        dcap = {}
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML,\
            like Gecko) Chrome/56.0.2924.76 Safari/537.36/")
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)


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
