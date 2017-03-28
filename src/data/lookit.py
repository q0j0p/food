import numpy as np
import pymongo
import pandas as pd
# Connection to Mongo DB and import recipe and ingredients collections as Pandas
try:
conn=pymongo.MongoClient()
print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
print "Could not connect to MongoDB: %s" % e
conn
recipesdb = conn['allrecipes']
collection = recipesdb['recipes']
collection2 = recipesdb['ingredients']
df = pd.DataFrame(list(collection.find()))
df2 = pd.DataFrame(list(collection2.find()))
df2 = df2.set_index('idnumber')
df = df.set_index('idnumber')
import re
#convert times to minutes
def contomin(timetest):
if timetest == 'NA':
return ''
if re.search('D', timetest):
days = int(re.findall('(\d+)D', timetest)[0])
else:
days = 0
if re.search('H', timetest):
hours = int(re.findall('(\d+)H', timetest)[0])
else:
hours = 0
if re.search('M', timetest):
minutes = int(re.findall('(\d+)M', timetest)[0])
else:
minutes = 0
return minutes+hours*60+days*60*24
#convert made it counter from units of K's into thousands
def madetocountfix(madecount):
if re.search('K', madecount):
madecount = re.sub('K', '000', madecount)
return int(madecount)
#convert counter from K's to thousands and convert times into minutes
df.made_it_count = map(madetocountfix,df.made_it_count)
df['cook_time'] = map(contomin, df.cook_time)
df['prep_time'] = map(contomin, df.prep_time)
df['total_time'] = map(contomin, df.total_time)
#Convert panda data frames into text files
df.to_csv('recipespd.txt',sep='\t')
df2.to_csv('ingredientspd.txt',sep='\t')
- See more at: http://blog.nycdatascience.com/student-works/recipes-scraping-top-20-recipes-allrecipes/#sthash.07jO2fJT.dpuf
