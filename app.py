import json
import pymongo
import User_Functions
import sys
import utilities

# static user id
USER_ID = "H5nQxTo0L2uOGlwDvbFVKf"


def main():
    # connect to mongodb server
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # populate database if not exists
    populate_data(client)

    while True:
        print("\n****************************************************")
        print("***** Welcome to Business Details Application ******")
        print("****************************************************\n")
        print("1.Find Business by Name")
        print("2.Give/Delete Business Rating")
        print("3.Find Businesses by State and City")
        print("4.Find Businesses by Categories")
        print("5.Sort Businesses by Categories and Ratings")
        print("6.Check Business's open hours")
        print("7.Find Business's tips")
        print("8.Check Business's address")
        print("9.Check if Business is Open or Closed")
        print("10.Find Average Star, Rating Count")
        print("11.Filter Specific Rating Reviews")
        print("12.Business Checkin")
        print("13.Find Number of Check-ins")
        print("14.Find Reviews of Business")
        print()
        select = input('Choose your option or terminate this application by typing quit: ')
        print()
        if select == "quit":
            print("Goodbye!")
            break
        elif select == "1":
            find_business()
        elif select == "2":
            give_delete_business_ratings()
        elif select == "3":
            User_Functions.browse_state_city()
        elif select == "4":
            User_Functions.browse_categories()
        elif select == "5":
            User_Functions.sort_by_ratings()
        elif select == "6":
            User_Functions.check_hours()
        elif select == "7":
            User_Functions.find_tips()
        elif select == "8":
            User_Functions.find_address()
        elif select == "9":
            User_Functions.check_open() 
        elif select == "10":
            User_Functions.find_rating()
        elif select == "11":
            User_Functions.filter_reviews()
        elif select == "12":
            User_Functions.checkin()
        elif select == "13":
            User_Functions.count_checkin()
        elif select == "14":
            User_Functions.find_reviews()
        else:
            print("Invalid option. Please choose again!")

    # close connection
    client.close()

def find_business():
    while True:
        print("***** Find Business by Name *****")
        print("1.Find business with full name")
        print("2.Find business with partial name")
        print()
        select = input('Choose your option or type "back" or "quit": ')
        if select == "quit":
            print("Goodbye!")
            sys.exit()
        elif select == "back":
            break
        elif select is "2":
            User_Functions.find_business_based_on_name_partial()
        elif select is "1":
            User_Functions.find_business_based_on_name_full()
        else:
            print("Invalid option. Please choose again!")


def give_delete_business_ratings():
    while True:
        print("***** Give/Delete Business Ratings *****")
        print("1.Give Business Ratings")
        print("2.Delete Business Ratings")
        print()
        select = input('Choose your option or type "back" or "quit": ')
        if select == "quit":
            print("Goodbye!")
            sys.exit()
        elif select == "back":
            break
        elif select is "1":
            User_Functions.give_business_rating()
        elif select is "2":
            User_Functions.delete_business_rating()
        else:
            print("Invalid option. Please choose again!")


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
            '../small_yelp_dataset/checkin.json', 'r')]
        checkin_col.insert_many(checkin)

        print("Done populating the database")


if __name__ == "__main__":
    main()
