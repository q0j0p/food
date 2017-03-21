
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
`MongoDB pseudo-schema: 
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
                   `

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


## Allrecipes.com 
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

## Principles 
* promote cooking, use of fresh ingredients, sustainable healthy living 
* recommendations populate weekly schedule 
* anti deprivation: abundance of options to create wholesome eating choices.  

### References 
[Cooksmarts](https://www.cooksmarts.com/weekly-meal-plan-service/)

