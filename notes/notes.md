
Gather all data from UDSA NDB database: 

-capture error msg when gathering NDB API data  

```Traceback (most recent call last):
  File "ndb_to_mongo.py", line 26, in <module>
    coll.insert_many(t.json()['list']['item'])
    
KeyError: 'list'
HTTP stats code is 429: Too many requests.  
```

-find out difference between food list and food items. 

## Mongodb and pymongo 

## t2.micro instantiation, setup for scraping 
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

