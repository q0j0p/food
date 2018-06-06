# Notes, code snippets, etc. taken during the project
--dynamic and unordered by nature 

## Data collection 

Gather all data from UDSA NDB database: 

-capture error msg when gathering NDB API data  

```Traceback (most recent call last):
  File "ndb_to_mongo.py", line 26, in <module>
    coll.insert_many(t.json()['list']['item'])
    
KeyError: 'list'
HTTP stats code is 429: Too many requests.  
```



## Mongodb and pymongo 

MongoDB pseudo-schema: 
```
db = client.allrecipes 
db.members.insert({"member_ID" : str member_ID, 
                   "link" : str link,
                   "faviorites" : list favorite, 
                   "madeit" : list made_it, 
                   "reviews" : list reviews, 
                   "personals" : list personal_recs, 
                   "followers" : list followers, 
                   "following" : list following, 
                   "contacted" : list contacted})
```


* The "community" page of allrecipes.com was scraped, generating > 4500 entries with > 900 unique members.  
* The member's individual pages were scraped.  These have sections-- 'favorites', 'reviews', 'personal-recipes', 'made-it', 'followers', and 'following'.  
* All recipes mentioned in these pages were scraped.  
* Scraped data were parsed and pertinent data was extracted and stored in a MongoDB database.  

## S3 storage 
Initially, the mongoDB database running on my local machine was the main repository for scraped data.  But with the use of EC2 instances, an S3 bucket was used to store scraped pages, both as backup (having overwritten an entire mongoDB collection at least once) and as an intermediary between EC2 and the local machine. 

- path `member_pages/` corresponds to allrecipes_db.member_pages collection.  


## AWS EC2 
### t2.micro instantiation, setup for scraping 
Steps: 

[Instantiate EC2] 

ssh -i ~/.ssh/jgalv2.pem  ubuntu@ec2-54-200-187-213.us-west-2.compute.amazonaws.com

sudo apt-get install install mongodb 

sudo apt install python-pip

tmux 

sudo apt-get update 

sudo apt install python-pip

pip install conda 

pip install -- upgrade pip 

wget https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh

bash Anaconda2-4.1.1-Linux-x86_64.sh

[install procedure] 

source .bashrc

restore tmux after computer reboot: `tmux a`

### phantomjs 
- Download phantomjs and uncompress

`sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2`
`sudo tar xjf phantomjs-1.9.7-linux-x86_64.tar.bz2`
- Create links 

`sudo ln -s /usr/local/share/phantomjs-1.9.7-linux-x86_64/bin/phantomjs /usr/local/share/phantomjs`
`sudo ln -s /usr/local/share/phantomjs-1.9.7-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs`
`sudo ln -s /usr/local/share/phantomjs-1.9.7-linux-x86_64/bin/phantomjs /usr/bin/phantomjs`
- Fix for error ( cannot open shared object file: No such file or directory): 

`sudo apt-get install libfontconfig`

On EC2 instance ([ref](https://www.codeammo.com/article/install-phantomjs-amazon-linux))

** Make sure phantomjs version is up to date (currently 2.1.1)! ** 

### To get matplotlib to work[ref](https://askubuntu.com/questions/276281/how-do-i-configure-matplotlib-to-work-on-ec2): 
```
pip uninstall matplotlib           //unistall matplotlib
apt-get build-dep matplotlib       //download and build needed dependencies
pip install -U matplotlib          //force matplotlib rebuild
```


## Web app development  
* `'flask'`- python based micro framework for web applications
* `'jinja2'`- templating language for python 
* `'bootstrap'` for front end (html, css, javascript) [here](https://www.w3schools.com/bootstrap/bootstrap_templates.asp)
  * [marketing template](https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_temp_marketing&stacked=h) 
  * [Simple one page template](https://startbootstrap.com/template-overviews/one-page-wonder/)

Structure: 
  * templates 
  * static 


# Allrecipes.com 
- The most popular English-langauge food websie in the world.  50 million visits in December.  

Articles 

[link](http://www.slate.com/articles/life/food/2016/05/allrecipes_reveals_the_enormous_gap_between_foodie_culture_and_what_americans.html)

 
 ## 

## Characterizing allrecipes members: 

Categories: 
* all members are 'cooks' 

* \# of followers 
* \# of favorites 
* \# of recipes made 

# Motivations 

The US spends the majority of its healthcare budget on preventable "lifestyle" chronic diseases ($ 1.5 trillion per year), more than any other nation, with predictable increasing trends.  In spite of live an ever increasing body of information on healthy living, the way we absorb and implement insights from knowledge is evidently lacking.  While this is attributable to various commercial and social factors, it is at least in part a "data science" problem, and part of the solution is to equip the user with more data-based tools that are shaped to effectively modify lifestyle choices.  

On the issue of nutrition, 

## Principles 
* promote cooking, use of fresh ingredients, sustainable healthy living 
* recommendations populate weekly schedule 
* anti deprivation: abundance of options to create wholesome eating choices.  

### References 

#### Concept
- [Cooksmarts](https://www.cooksmarts.com/weekly-meal-plan-service/)  

#### Types of recommenders
* recommendation based on content 
* recommendation based on preferences 
* collaborative filtering based on similarity 

### Recommender modeling 
* Explicit and implicit feedback 
* UV Decomposition


* Item item similarity * 

* Matrix factorization 


#### User 'cold start' 

Typical recommener systems need to deal with the cold start problem, whn user preferences are not known.  This isn't necessarily an issue for this recommender as a questionnaire is part of the onboarding process, and the outcome is exploratory.  

#### User questionnaire 

#### Recommeder evaluation 
Recommenders are inherenty hard to validate.  In this application, validation is less crucial, but user feedback can be reintroduced as a factor in subsequent user iterations to derive a heuristic that meets the success criteria of the user in achieving a wholesome nutrition lifestyle.  


- [Recipe recommendation using ingredient networks](http://lazerlab.net/publication/recipe-recommendation-using-ingredient-networks)
- [Amazon fine food reviews](https://snap.stanford.edu/data/web-FineFoods.html) 

## Data Processing 
### Natural language processing 

Build separate corpuses for review, recipe, about-me, conversations documents.  
Construct tf-idf vectors 

* Tokenize ingredients, use tf-idf to characterize recipes 

## USDA nutritional database 

- Create tfidf with ingredients list for each food item 
- Evaluate tfidf feature matrix 
- t2.doublexl instance isn't big enough for affinity propagation.  
- m4.4xlarge is still not big enough 
- this is partially due to bad tokenization of ingredients (permutations in spelling, etc.).  Create tokenizer for tfidf to remove artifacts and consolidate terms.  

**Attempts to perform affinity propagation were unscuccessful thus far-- failure to converge**  



### Issues

- How meaningful / useful are the topics derived with LDA?  
- What is a good, quantifiable definition of "healthy" or "wholesome"?  
  - For each meal: 
    - Use of whole ingredients 
    - Less saturated fats 
  - For weekly schedule of meals: 
    - "balancing out" of nutritional requirements
    - Complete nutrition 


## Linking topics derived from LDA of USDA food items to recipes  

* Parse recipe ingredient list 
* 

|Source|Pages scraped |   |
|---|---|---|
|allrecipes.com|   |   |
|USDA|   |   |


---
## User onboarding 
### Questionnaire 
  * prompt user to list 1 week history of meals.  
    * user rates each meal


## Parsing ingredients list 

[This article](https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/?_r=0) is insightful for parsing ingredients. 

* The USDA branded items list contains list of ingredients for each food item, in a format typically seen on labels.  Use of punctuation is not consistent.  


* Recipe datasets have ingredients lists that are typically composed of "quantity-unit-item" phrases.  



