
# Organize allrecipes database 
- Create appropriate unique indices (based on recipe_ID, member_ID, etc. ) 
- Check number of documents

# Issues: 
- There is a 20 item limit for each webpage pertaining to a member (e.g. "favorites": maximum of 20 are displayed on page).  


```python
import pymongo 
client = pymongo.MongoClient("mongodb://localhost:27017/")
allrecipes_db = client.allrecipes
member_pages_coll = allrecipes_db.member_pages
members_coll = allrecipes_db.members
recipes_coll = allrecipes_db.recipes
about_coll = allrecipes_db.about
```


```python
# Create appropriate unique indices (based on recipe_ID, member_ID, etc. )
# member_pages_coll.create_index([('member_ID',pymongo.ASCENDING)], unique=True)
# members_coll.create_index([('member_ID',pymongo.ASCENDING)], unique=True)
# recipes_coll.create_index([('recipe_ID',pymongo.ASCENDING)], unique=True)
```


```python
print member_pages_coll.count()
print members_coll.count()
print recipes_coll.count()

```

    1430
    1430
    11111



```python
member_page_keys = member_pages_coll.find_one().keys()
```


```python
member_page_keys
```




    [u'favorites_page',
     u'following_page',
     u'reviews_page',
     u'aboutme_page',
     u'madeit_page',
     u'link',
     u'member_ID',
     u'followers_page',
     u'_id',
     u'recipes_page']




```python
member_keys = members_coll.find_one({'followers_dict':{"$exists":True}}).keys()
member_keys
```




    [u'nutrition',
     u'followers_dict',
     u'reviews_dict',
     u'following_id_list',
     u'madeits_recipe_id_list',
     u'favorites_dict',
     u'reviews_recipe_id_list',
     u'nutrition_avg_vals',
     u'following_dict',
     u'member_ID',
     u'favorites_recipe_id_list',
     u'_id',
     u'aboutme',
     u'madeits_dict',
     u'followers_id_list']




```python
recipe_keys = recipes_coll.find_one().keys()
recipe_keys
```




    [u'Cholesterol',
     u'nutrition',
     u'Carbs',
     u'recipe_times',
     u'nutrition_elements',
     u'Sodium',
     u'name',
     u'nutrition_serving_info',
     u'description',
     u'Calories',
     u'Fat',
     u'servings_config',
     u'recipe_ID',
     u'rating_list',
     u'servings',
     u'nutrition_info',
     u'Protein',
     u'_id',
     u'page',
     u'directions_list',
     u'ingredients_list']




```python
member_essentials = set(member_keys) - set(member_page_keys)
```


```python
# These are the field required fomr members
member_essentials
```




    {u'aboutme',
     u'favorites_dict',
     u'favorites_recipe_id_list',
     u'followers_dict',
     u'followers_id_list',
     u'following_dict',
     u'following_id_list',
     u'madeits_dict',
     u'madeits_recipe_id_list',
     u'nutrition',
     u'nutrition_avg_vals',
     u'reviews_dict',
     u'reviews_recipe_id_list'}




```python
pages_list = [a['member_ID'] for a in member_pages_coll.find({"member_ID":{"$exists":True}})]
mems_list = [a['member_ID'] for a in members_coll.find({"member_ID":{"$exists":True}})]
```


```python
hit_list = set(pages_list) - set(mems_list)
```


```python
len(hit_list)
```




    0




```python
r_hit_list = set(mems_list) - set(pages_list)
```


```python
len(r_hit_list)
```




    0




```python
import sys 
sys.path.insert(0,'../..')
import main
import inspect
# Get list of methods in `scraper`
[a[0] for a in inspect.getmembers(main.Scraper, inspect.ismethod)]
```




    ['__init__',
     'get_community_members',
     'get_community_members_continue',
     'get_community_page_scrolled',
     'get_member_pages',
     'get_page_from_list',
     'use_firefox',
     'use_phantom']




```python
# Get list of methods in `Parser`
[a[0] for a in inspect.getmembers(main.Parser, inspect.ismethod)]
```




    ['__init__',
     'check_member_records',
     'get_aboutme_data',
     'get_all_member_nutrition_values',
     'get_favorites_data',
     'get_followers_data',
     'get_following_data',
     'get_madeits_data',
     'get_member_list_to_parse',
     'get_member_nutrition_summary',
     'get_member_nutrition_values',
     'get_member_parsed_data',
     'get_members_aboutme_from_pkl',
     'get_members_coll_info',
     'get_members_favorites',
     'get_members_followers',
     'get_members_following',
     'get_members_madeits',
     'get_members_reviews',
     'get_recipe_data',
     'get_recipe_data_from_recipe_pages_coll',
     'get_recipe_nutrition',
     'get_recipe_pkl_page_from_aws',
     'get_recipes_coll_info',
     'get_reviews_data',
     'insert_all_nutrition_info',
     'parse_recipe_data']




```python
parser1 = main.Parser()
```

    Connected to Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), u'allrecipes')



```python
parser1.get_members_coll_info()
```

    number of member_pages: 1430
    number of docs with member_IDs: 1430
    number of docs with followers_dict 1430
    number of docs with following_dict 1430
    number of docs with reviews_dict 1430
    number of docs with favorites_dict 1430
    number of docs with madeits_dict 1430
    number of docs with aboutme 1430
    number of docs with nutrition values 1430



```python
parser1.get_recipes_coll_info()
```

    number of documents: 11111
    number of docs with pages: 9023
    number of docs with nutrition_info 11111
    number of docs with directions 10831
    number of docs with rating_list 10831
    number of docs with nutrition_elements 9757
    number of docs with itemized nutrition 9757
    number of docs with ingredients_list 10831

