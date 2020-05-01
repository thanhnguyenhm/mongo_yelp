import pymongo
import sys
import app
import utilities
import datetime
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")

# get collections from database
db = client["yelp_database"]
business_col = db['business']
review_col = db['review']
user_col = db['user']
checkin_col = db['checkin']
tip_col = db['tip']


def find_business_based_on_name_full():
    """
    Find business based on full name
    Use Case 1
    """
    while True:
        print()
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        print_business(business_object)


def find_business_based_on_name_partial():
    """
    Find business based on partial name
    Use Case 2
    """
    while True:
        print()
        business_name = input(
            'Please enter partial business name or type "back" or "quit": ')
        print()
        if business_name == "quit":
            print("Goodbye!")
            sys.exit()
        if business_name == "back":
            return

        business_objects = business_col.find(
            {"$text": {"$search": business_name}}).limit(10)
        if business_objects is None:
            print("No business found with given name.")
            continue

        for business_object in business_objects:
            print_business(business_object)


def browse_state_city():
    """
    Find businesses based on State and Ciy
    Use Case 3
    """
    print("***** Find Businesses by State and City *****")
    while True:
        print()
        state = input(
            'Please enter a state abbreviation or type "back" or "quit": ')
        print()
        if state == "quit":
            print("Goodbye!")
            sys.exit()
        if state == "back":
            return
        city = input('Please enter a city name: ')

        cursor = business_col.find(
            {"state": state, "city": city})

        business_objects = cursor.limit(10)
        if cursor.count() == 0:
            print("No business found with given state and city.")
            continue

        for business_object in business_objects:
            print_business(business_object)


def browse_categories():
    """
    Find businesses based on categories
    Use Case 4
    """
    print("***** Find Businesses by Categories *****")
    while True:
        print()
        category = input(
            'Please enter a type of business (category) or type "back" or "quit": ')
        print()
        if category == "quit":
            print("Goodbye!")
            sys.exit()
        if category == "back":
            return

        # create a regex pattern for business name
        pattern = r".*" + re.escape(category) + r".*"
        regx = re.compile(pattern, re.IGNORECASE)

        cursor = business_col.find({"categories": regx})

        business_objects = cursor.limit(10)
        
        if cursor.count() == 0:
            print("No businesses found with given category.")
            continue
        for business_object in business_objects:
            print_business(business_object)


def sort_by_ratings():
    """
    Sort businesses based on ratings descending when searching by category
    User case 5
    """

    print("***** Find Businesses by Categories Sorted by Rate *****")
    while True:
        print()
        category = input(
            'Please enter a type of business (category) or type "back" or "quit": ')
        print()
        if category == "quit":
            print("Goodbye!")
            sys.exit()
        if category == "back":
            return

        # create a regex pattern for business name
        pattern = r".*" + re.escape(category) + r".*"
        regx = re.compile(pattern, re.IGNORECASE)

        cursor = business_col.find({"categories": regx})

        business_objects = cursor.limit(10).sort("stars", -1)

        if cursor.count() == 0:
            print("No businesses found with given category.")
            continue
        for business_object in business_objects:
            print(f'Stars: {business_object["stars"]}')
            print_business(business_object)


def check_hours():
    """
    Allow users to check open hours of given business
    User case 6
    """
    while True:
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        print(f"{business_object['name']} hours are: "
              f"{business_object['hours']}")


def find_tips():
    """
    Allow users to see tips of given business
    User case 7
    """
    while True:
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue
        id = business_object['business_id']
        tip_object = tip_col.find({"business_id": id}).limit(10)
        print(f"{business_object['name']} tips are: ")
        for tip in tip_object:
            print(tip["text"])


def find_address():
    """
    Allow users to check address of given business
    User case 8
    """
    while True:
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        print(f'{business_object["name"]}\'s address is:'
              f'{business_object["address"]}, {business_object["city"]} '
              f'{business_object["state"]}')


def check_open():
    """
    Check if a business is open
    Use Case 9
    """
    print("***** Check if Business is Open/Closed *****")
    while True:
        print()
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        if business_object['is_open'] == 1:
            print("This business is open!")
        else:
            print("This business is closed!")

        print()

        print_business(business_object)


def find_rating():
    """
    Find average star and total rating counts
    Use Case 10
    """
    print("***** Finding Star/Rating *****")
    while (True):
        print()
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        print("This business is rated " + str(
            business_object['stars']) + " stars with " + str(
            business_object['review_count']) + " reviews.\n")

        print_business(business_object)


def give_business_rating():
    """
    Give a rating to the business
    Use Case 11
    """
    print("***** Adding Rating *****")
    while (True):
        print()
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        print_business(business_object)

        print()

        business_rating = float(input(
            'Please enter your rating for ' + business_object['name'] + ": "))
        comment = input(
            'Please enter your comments for ' + business_object['name'] +
            ' or type "back" or "quit": ')
        print()
        if comment == "quit":
            print("Goodbye!")
            sys.exit()
        if comment == "back":
            return

        print()
        review_col.insert({"review_id": utilities.random_rating_id(),
                           "user_id": app.USER_ID,
                           "business_id": business_object['business_id'],
                           "stars": business_rating,
                           "date": datetime.datetime.today(),
                           "text": comment,
                           "useful": 0,
                           "funny": 0,
                           "cool": 0})
        print('Thank you for providing your rating for ' +
              business_object['name'])


def checkin():
    """
    Allow users to check-in at the business
    Use Case 13
    """
    print("***** Checking In *****")
    while True:
        print()
        business_name = input(
            'Please enter partial business name to check-in or type "back" or '
            '"quit": ')
        print()
        if business_name == "quit":
            print("Goodbye!")
            sys.exit()
        if business_name == "back":
            return

        business_object = business_col.find(
            {"$text": {"$search": business_name}}).limit(10)
        if business_object is None:
            print("No business found with given name.")
            continue
        postal_code_list = []
        for bus in business_object:
            postal_code_list.append(bus['postal_code'])
            print(
                f'Business name: {bus["name"]}, City: {bus["city"]}, Postal Code: 'f'{bus["postal_code"]}')

        # input postal code to choose which business to check in
        # same business_name can have multiple locations
        postal_code = 0
        while postal_code not in postal_code_list:
            postal_code = input('Postal code or "back": ')
            if postal_code == 'back':
                return
        store = business_col.find_one(
            {"$text": {"$search": business_name}, "postal_code": postal_code})

        print()
        date = datetime.datetime.now()
        checkin_col.update({"business_id": store['business_id']},
                           {"$push": {
                               "date": date.strftime("%Y-%m-%d %H:%M:%S")}})
        print(f'Thank you for checking in at {store["name"]}-{postal_code}')

def count_checkin():
    """
    Count how many people have checked in at a business
    Use case 14
    """
    print("***** Find Number of Checkins *****")
    while (True):
        print()
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        id = business_object['business_id']
        checkin_object = checkin_col.find({"business_id": id})

        for checkin in checkin_object:
            num = len(checkin['date'].split(","))
        
        print(f'This business has {num} check-ins.')


def find_reviews():
    """
    See all reviews of a business
    Use Case 15
    """
    print("***** Find Reviews of a Business *****")
    while (True):
        print()
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue
        id = business_object['business_id']
        review_object = review_col.find({"business_id": id}).limit(10)
        print(f'{business_object["name"]} has'
              f' {business_object["review_count"]} '
              f'reviews:')
        for review in review_object:
            userid = review['user_id']
            username = user_col.find({"user_id": userid})
            print(f'- {username} ({review["stars"]}):'
                  f' {review["text"]}.'
                  f' {review["date"]}')


def delete_business_rating():
    """
    Delete rating to the business from userID
    Use Case 16
    """
    print("***** Deleting Rating *****")
    while True:
        print()
        business_object = query_business_name()
        if business_object == "back":
            return
        elif business_object is None:
            continue

        print("Please wait...")

        # find review using business id and user id
        business_id = business_object['business_id']
        review_obj = review_col.find_one({"user_id": app.USER_ID})

        if review_obj:
            print('This is your review for ' + business_object['name'] + ': ')
            print('Stars: ' + str(review_obj['stars']))
            print('Review: ' + review_obj['text'])

            choice = input(
                '\nDo you want to delete this review? Type "yes" to delete, type "back" to go back: ')
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


def print_business(business_object):
    """
    Helper function to print business details
    """
    # OLD ----------
    # print('Business name: ' + business_object['name'])
    # print('Address: ' + business_object['address'])
    # print('City: ' + business_object['city'])
    # print('State: ' + business_object['state'])
    # print('Average Ratings: ' + str(business_object['stars']) +
    #       ' Review Count: ' + str(business_object['review_count']))
    # print('categories: ' + str(business_object['categories']))

    print(business_object['name'])
    print(f'Address: {business_object["address"]}, '
          f'{business_object["city"]}, {business_object["state"]}')
    print('#############################')


def query_business_name():
    """
    Helper function to query full business name
    Return a Mongo object
    """
    print()
    business_name = input(
        'Please enter full business name or type "back" or "quit": ')
    print()
    if business_name == "quit":
        print("Goodbye!")
        sys.exit()
    if business_name == "back":
        return "back"

    business_object = business_col.find_one({"name": business_name})
    if business_object is None:
        print("No business found with given name.")

    return business_object
