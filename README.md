This project frames the health crisis as a data science problem and explores a practical, "data driven" solution in the form of a recipe recommendation system.   

## Documentation 

* [Project proposal](https://docs.google.com/document/d/1fyTX7zHu0Tg92daD9yG4MbEVNJWpAo9V0dDwW1b2xGA/edit?usp=sharing)
* [Presentation](https://docs.google.com/presentation/d/1vTqdFdSiJ_m-carGSUVMQn9V2vPaHaKSxM-NFZ9JN2A/edit?usp=sharing) 
* [Notes](https://github.com/q0j0p/food_recommender/blob/master/notes/notes.md)

## Data 

### Data requirements 
* Nutritional data of food items 
  * Collected from USDA [Food composition database](https://ndb.nal.usda.gov/ndb/search/list) with API 
  * code:[src/data/ndb_to_mongo.py](src/data/ndb_to_mongo.py)
* Recipe and user data 
  * Recipes, ratings, member info scraped from [allrecipes.com](https://allrecipes.com) using selenium
  * code: [src/data/scraper.py](src/data/scraper.py)
  
### Data management 
* Main storage in MongoDB nosql database.  
 * Recipes, member info stored as documents in respective collections 
 

