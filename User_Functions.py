import pymongo
import sys
import app
import utilities
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")

# get collections from database
db = client["yelp_database"]
business_col = db['business']
review_col = db['review']
user_col = db['user']
checkin_col = db['checkin']


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


def give_business_rating():
    """
    Give a rating to the business
    """
    while(True):
        print()
        business_name = input(
            'Please enter full business name to give Ratings or type "back" or "quit": ')
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
        print('categories: ' + str(business_object['categories']))

        print()

        business_rating = float(input('Please enter your rating for ' + business_object['name'] +
                                      ' or type "back" or "quit": '))
        comment = input('Please enter your comments for ' + business_object['name'] +
                        ' or type "back" or "quit": ')
        print()
        if business_rating == "quit":
            print("Goodbye!")
            sys.exit()
        if business_rating == "back":
            return

        print()
        review_col.insert({ "review_id": utilities.random_rating_id(),
                                "user_id": app.USER_ID,
                                "business_id": business_object['business_id'],
                                "stars": business_rating,
                                "date": datetime.datetime.today(),
                                "text": comment,
                                "useful": 0,
                                "funny": 0,
                                "cool": 0})
        print('Thank you for providing your rating for ' + business_object['name'])


def delete_business_rating():
    """
    Delete rating to the business from userID
    """
    while(True):
        print()
        business_name = input(
            'Please enter full business name to delete Ratings or type "back" or "quit": ')
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

        # find review using business id and user id
        business_id = business_object['business_id']
        review_obj = review_col.find_one({"user_id": app.USER_ID})

        
        if review_obj:
            print('This is your review for ' + business_object['name'] + ': ')
            print('Stars: ' + str(review_obj['stars']))
            print('Review: ' + review_obj['text'])

            choice = input('\nDo you want to delete this review? Type "yes" to delete, type "back" to go back: ')
            if choice == 'back':
                return
            elif choice == 'yes':
                review_col.remove(review_obj)
                print("\nYour review has been deleted!")
            else:
                print("Invalid choice")
                return
        else:
            print("You have no review for " + business_object['name'] + "\n")
            return
        print()


def checkin():
    while(True):
        print()
        business_name = input(
            'Please enter full business name to check-in or type "back" or '
            '"quit": ')
        print()
        if business_name == "quit":
            print("Goodbye!")
            sys.exit()
        if business_name == "back":
            return

        business_object = business_col.find({"name": business_name})
        if business_object is None:
            print("No business found with given name.")
            continue
        print(f'Business name: {bus["name"]}, City: {bus["city"]}, Postal Code: '
              f'{bus["postal code"]}' for bus in business_object)
        postal_code_list = [i for i in business_object["postal code"]]
        # input postal code to choose which business to check in
        # same business_name can have multiple locations
        postal_code = 0
        while postal_code not in postal_code_list:
            postal_code = input('Postal code or "back": ')
            if postal_code == 'back':
                return
        store = business_col.find_one({"name": business_name, "postal "
                                                                 "code": postal_code})
        date = datetime.datetime.now()
        print()
        # Update required version of date time
        checkin_col.insert({"business_id": store['business_id'],
                                "date": date.strftime("%Y-%m-%d %H:%M:%S")})
        print(f'Thank you for checking in at {business_object["name"]}-{postal_code}')
    print()
