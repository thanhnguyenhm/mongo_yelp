import json
import pymongo

def main():
    # connect to mongodb server
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # populate database if not exists
    populate_data(client)

    # get collections from database
    db = client["yelp_database"]
    business_col = db['business']
    review_col = db['review']
    user_col = db['user']

    # function 1
    function1(business_col)

    # function 2
    # function 3
    # function 4
    # function 5....

    # close connection
    client.close()


def function1(business_col):
    print(business_col.find_one())


def populate_data(client):
    if 'yelp_database' not in client.list_database_names():
        # create database
        db = client["yelp_database"]

        # create collections
        business_col = db['business']
        review_col = db['review']
        user_col = db['user']

        # import json data and insert to collection
        business = [json.loads(line) for line in open(
            '../yelp_dataset/yelp_academic_dataset_business.json', 'r')]
        business_col.insert_many(business)

        review = [json.loads(line) for line in open(
            '../yelp_dataset/yelp_academic_dataset_review.json', 'r')]
        review_col.insert_many(review)

        user = [json.loads(line) for line in open(
            '../yelp_dataset/yelp_academic_dataset_user.json', 'r')]
        user_col.insert_many(user)

        print("Done")

if __name__ == "__main__":
    main()
