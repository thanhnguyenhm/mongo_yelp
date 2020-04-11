import json
import pymongo
import User_Functions


def main():
    # connect to mongodb server
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # populate database if not exists
    populate_data(client)

    while True:
        print("Welcome to Business Details Application")
        print("1.Find Business by Name")
        print("2.Give Business Rating")
        select = input('Choose your option or terminate this application by typing quit: ')
        if select == "quit":
            break
        elif select is "1":
            find_business()
        elif select is "2":
            print("Business Rating Function")



    # close connection
    client.close()


def find_business():
    while True:
        print("Find Business by Name")
        print("1.Find business with full name")
        print("2.Find business with partial name")
        select = input('Choose your option or Go BACK by typing quit: ')

        if select == "quit":
            break
        elif select is "1":
            User_Functions.find_business_based_on_name()
        elif select is "2":
            print("Another User Function")
            #Still need to implement this function


def populate_data(client):
    if 'yelp_database' not in client.list_database_names():
        # create database
        db = client["yelp_database"]

        # create collections
        business_col = db['business']
        review_col = db['review']
        user_col = db['user']
        tip_col = db['tip']
        checkin_col = db['checkin']

        # import json data and insert to collection
        business = [json.loads(line) for line in open(
            '../small_yelp_dataset/business.json', 'r')]
        business_col.insert_many(business)

        review = [json.loads(line) for line in open(
            '../small_yelp_dataset/review.json', 'r')]
        review_col.insert_many(review)

        user = [json.loads(line) for line in open(
            '../small_yelp_dataset/user.json', 'r')]
        user_col.insert_many(user)

        tip = [json.loads(line) for line in open(
            '../small_yelp_dataset/tip.json', 'r')]
        tip_col.insert_many(tip)

        checkin = [json.loads(line) for line in open(
            '../small_yelp_dataset/tip.json', 'r')]
        checkin_col.insert_many(checkin)

        print("Done populating the database")


if __name__ == "__main__":
    main()
