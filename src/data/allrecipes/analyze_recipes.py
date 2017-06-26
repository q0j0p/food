import pymongo
import re
import pandas as pd
import numpy as np

client = pymongo.MongoClient('mongodb://localhost/27017')
allrecipes_db = client.allrecipes
recipes_coll = allrecipes_db.recipes
members_coll = allrecipes_db.members
about_coll = allrecipes_db.about

# calories, sodium, fat, protein, carbs
#
def get_recipe_nutrition(rec):
    """Extracts nutrition info from scraped text `nutrition_info`, a field in recipes_coll.
    Scraper captures calorie, fat, protein, carb, sodium info from recipes as text.
    Uses patterns in string to return key-value pairs for each nutrient.
    Use regular expressions to select item, quantity, unit:
        Divide string by  ":"
        Take the alphanumeric string to the left of : as the item.
        Take numeric string to the right as quantity (it may inclide commas and periods).
        Take the final string as unit.


    Parameters
    ----------
    recipe_ID: str, ID of recipe

    Returns
    -------
    (key, value, unit) for each
    """
    q = re.compile('(?<=[\s:<])\d*\.?\,?\d+')
    u = re.compile('[A-z]+$')
    i = re.compile('\w+(?=[:])')
    strlist = [a['nutrition_info'] for a in recipes_coll.find({'recipe_ID':rec})]
    n_list = {}
    for a in strlist:
        for b in a:
                quantity = q.findall(b)
                unit = u.findall(b)
                item = i.findall(b)
                if quantity and unit and item:
#                    print item[0], float(quantity[0]), unit[0]
                    n_list[item[0]]=[float(quantity[0]), unit[0]]
    return n_list

def get_recipe_coll_nutrition():
    '''Insert nutrient info for all documents in `recipe_coll`'''
    rec_list = recipes_coll.find({'nutrition_info':{'$exists':True}},['recipe_ID'])
    for rec in rec_list:
        n_list = get_recipe_nutrition(rec['recipe_ID'])
    #        print "inserting {} into {}...".format(n_list.keys(), rec['_id'])
        if n_list:
            recipes_coll.update_one({'_id':rec['_id']}, {'$set':{'nutrition':n_list}}, upsert=True)

def get_member_avg_nutrition(member_ID):
    """"""
    nutrition = {}
    mem_doc = members_coll.find_one({"member_ID": member_ID})
    recipes_list = mem_doc['madeits_dict'].values() + mem_doc['favorites_dict'].values()
    num_recipes = len(recipes_list)
    for a in recipes_list:
        recipe_nutrition = recipes_coll.find_one({"recipe_ID": a})['nutrition']
#        print a, nutrition[a]
        nutrition[a] = {b[0]: b[1][0] for b in recipe_nutrition.items()}
    D_df = pd.DataFrame(nutrition).T
    return dict(D_df.mean())

def get_member_coll_nutrition():
    """Get average value for all nutrtion items in `members_coll`"""
    mem_cur = members_coll.find({'member_ID': {'$exists': True}})
    for member in mem_cur:
        print member.keys()
        print member['madeits_dict']
        member['nutrition_avg_vals'] = get_member_avg_nutrition(member['member_ID'])
        members_coll.save(member)

if __name__ == '__main__':
    get_member_coll_nutrition()
