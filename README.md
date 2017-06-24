
## Motivation
This project is an attempt to pose a pervasive social concern in a data science framework and provide insight using appropriate tools.  

## Problem definition
 <img align="left" src="https://github.com/q0j0p/food/blob/master/notes/resources/Screen%20Shot%202017-06-23%20at%205.14.46%20PM.png" width="300"> Mortality is inevitable and it befalls us all, but a third of all deaths are deemed premature.  Further, the majority of premature deaths is preventable, arising from voluntary lifestyle choices.  The World Health Organization has estimated that if the major risk factors for chronic disease were eliminated, at least 80% of all heart disease, stroke, and type 2 diabetes would be prevented, and more than 40% of cancer cases would be prevented ([ref](http://www.who.int/chp/chronic_disease_report/full_report.pdf)).  About half of all American adults have one or more preventable, diet-related chronic diseases, including cardiovascular disease, type 2 diabetes, and overweight and obesity ([ref](https://health.gov/dietaryguidelines/2015/guidelines/executive-summary/). Among the statistics of lifestyle factors related to chronic disease, early deaths due to diet and physical activity patterns stands out in the fact that has actually increased in recent years (from 14% to 18% of all early deaths, 1990 to 2010). Poor diet and activity patterns is now the leading cause of early deaths, and the direct and indirect cost of their consequences are staggering.  
<p>
There is no shortage of information pertaining to health in our digital age, yet it is apparent that the implicit value proposition of technology-- that it serves to improve our lives-- is not fully realized in the information age.  In America, in spite of greater knowledge and exorbitant expenditures in healthcare, statistical evidence reveals that the returns are not evident in the general population.  Rather, as a population, we make voluntary choices that make us less healthy.  Numerous reasons exist for this epidemic, but to the extent that this is a data science problem, we must devise better data science tools to address the problem.  

The USDA and DHHS have conducted surveys on "What We Eat in America (WWEIA surveys) as well as analyses on nutrient compositions of foods consumed.  These bodies of knowledge form the basis for the dietary guidelines set forth every five years ([ref](https://health.gov/dietaryguidelines/2015/guidelines/executive-summary/)).  Their current recommendations emphasize principles that guide healhty eating patterns over time ([ref](https://health.gov/dietaryguidelines/2015/guidelines/executive-summary/#figure-es-1-2015-2020-dietary-guidelines-for-americans-at-a-glan)).  What can be done to empower individuals to adopt healthy eating habits?  

## Using data oriented methods to generate actionable insight  
<img align="right" src="notes/resources/doing_data_science_fig.png" width="300">Fundamentally, data science is about doing science with data that serves as the basis for delivering value in measurable form.  THe cross industry standard process for data mining ([CRISP-DM](https://en.wikipedia.org/wiki/Cross_Industry_Standard_Process_for_Data_Mining)) is a widely cited guideline for conducting data science.  

## Documentation
* [Project proposal](https://docs.google.com/document/d/1fyTX7zHu0Tg92daD9yG4MbEVNJWpAo9V0dDwW1b2xGA/edit?usp=sharing) morphing into project report
* Capstone [Presentation](https://docs.google.com/presentation/d/1vTqdFdSiJ_m-carGSUVMQn9V2vPaHaKSxM-NFZ9JN2A/edit?usp=sharing)
* [Notes](https://github.com/q0j0p/food_recommender/blob/master/notes/notes.md) on procedures

## Data
### Data requirements
* Nutritional data of food items
  * Collected from USDA [Food composition database](https://ndb.nal.usda.gov/ndb/search/list) with API
    * [src/data/ndb_to_mongo.py](src/data/ndb_to_mongo.py)
* Recipe and user data
  * Recipes, ratings, member info scraped from [allrecipes.com](https://allrecipes.com) using `selenium`
    * [src/data/scraper.py](src/data/scraper.py)

### Data management
* Main storage in `MongoDB` nosql database.  
 * Recipes, member info stored as documents in respective collections
 * Use of AWS/EC2 instances for scalability
   * [EC2_scraper.py](src/data/EC2_scraper.py)
   * Scraped data stored in S3 bucket



## Analysis and modeling
Code stored in [src/model](src/model/)
* EDA of USDA standard reference database
* Topic modeling of USDA branded items database
