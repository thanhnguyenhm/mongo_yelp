import pymongo
import sys
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")

# get collections from database
db = client["yelp_database"]
business_col = db['business']
review_col = db['review']
user_col = db['user']

def find_business_based_on_name_partial():
    """
    Find business based on partial name
    """
    while(True):
        print()
        business_name = input(
            'Please enter partial business name or type "back" or "quit": ')
        print()
        if business_name == "quit":
            print("Goodbye!")
            sys.exit()
        if business_name == "back":
            return

        business_objects = business_col.find({"$text": {"$search": business_name}}).limit(10)
        if business_objects is None:
            print("No business found with given name.")
            continue

        for business_object in business_objects:
            print('Business name: ' + business_object['name'])
            print('Address: ' + business_object['address'])
            print('City: ' + business_object['city'])
            print('State: ' + business_object['state'])
            print('Average Rating: ' + str(business_object['stars']) + ' Review Count: ' + str(business_object['review_count']))
            print('categories: ' + str(business_object['categories']))
            print('#############################')


def find_business_based_on_name_full():
    """
    Find business based on full name
    """
    while(True):
        print()
        business_name = input(
            'Please enter full business name or type "back" or "quit": ')
        print()
        if business_name == "quit":
            print("Goodbye!")
            sys.exit()
        if business_name == "back":
            return

        business_object = business_col.find_one({"name": business_name})
        if business_object is None:
            print("No business found with given name.")
            continue
        print('Business name: ' + business_object['name'])
        print('Address: ' + business_object['address'])
        print('City: ' + business_object['city'])
        print('State: ' + business_object['state'])
        print('Average Ratings: ' + str(business_object['stars']) +
              ' Review Count: ' + str(business_object['review_count']))
        print('categories: ' + str(business_object['categories']))
