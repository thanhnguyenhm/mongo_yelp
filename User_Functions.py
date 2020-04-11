import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

# get collections from database
db = client["yelp_database"]
business_col = db['business']
review_col = db['review']
user_col = db['user']


def find_business_based_on_name():
    business_name = input('Please enter business full name or GO BACK(type quit): ')
    if business_name == "quit":
        return

    business_object = business_col.find_one({"name": business_name})
    if business_object is None:
        print("NO Business found with given name. Try Business finder with partial business name")
        return
    print('Business name: ' + business_object['name'])
    print('Address: ' + business_object['address'])
    print('City: ' + business_object['city'])
    print('State: ' + business_object['state'])
    print('Average Ratings: ' + str(business_object['stars']) + ' Review Count: ' + str(business_object['review_count']))
    print('categories: ' + str(business_object['categories']))
    #calling back same function
    find_business_based_on_name()
    return


def function2():
    print(business_col.find_one())