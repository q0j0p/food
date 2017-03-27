
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

## Data collection 

* The "community" page of allrecipes.com was scraped, generating > 4500 entries with > 900 unique members.  
* The member's individual pages were scraped.  These have sections-- 'favorites', 'reviews', 'personal-recipes', 'made-it', 'followers', and 'following'.  
* All recipes mentioned in these pages were scraped.  
* Scraped data were parsed and pertinent data was extracted and stored in a MongoDB database.  


## AWS
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

#### Recommender modeling 
- [Recipe recommendation using ingredient networks](http://lazerlab.net/publication/recipe-recommendation-using-ingredient-networks)
- [Amazon fine food reviews](https://snap.stanford.edu/data/web-FineFoods.html) 

#### Types of recommenders
* recommendation based on content 
* recommendation based on preferences 
* collaborative filtering based on similarity 

* Item item similarity * 

#### User 'cold start' 

Typical recommener systems need to deal with the cold start problem, whn user preferences are not known.  This isn't necessarily an issue for this recommender as a questionnaire is part of the onboarding process, and the outcome is exploratory.  

#### User questionnaire 

#### Recommeder evaluation 
Recommenders are inherenty hard to validate.  In this application, validation is less crucial, but user feedback can be reintroduced as a factor in subsequent user iterations to derive a heuristic that meets the success criteria of the user in achieving a wholesome nutrition lifestyle.  

