#!/Users/vineetbhatia/ENV/bin/python -tt

import json 
import requests
import urllib2
import argparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_business_id(url, headers, params):
    r = requests.request('GET', url, headers=headers, params=params)
    dict_out =  r.json()
    for k, v in dict_out.items():
        if isinstance(v, list):
            if 'categories' not in params.keys():
                my_dict = v[0]
                category_dict = my_dict['categories'][0]
                my_restaurant_dict = {my_dict['id']: [my_dict['name'], category_dict['title'], my_dict['rating'],my_dict['location']['display_address'], my_dict['display_phone']]}
                for key in my_restaurant_dict:
                    url = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(key)
                    name = my_restaurant_dict[key][0]
                    cuisine = my_restaurant_dict[key][1]
                    rating = my_restaurant_dict[key][2]
                    address = my_restaurant_dict[key][3]
                    phone = my_restaurant_dict[key][4]
                    get_business_review(name, cuisine, rating, address, phone, url, headers)
            else:
                for items in v:
                    if isinstance(items, dict):
                        my_dict = items
                        category_dict = my_dict['categories'][0]
                        my_restaurant_dict = {my_dict['id']: [my_dict['name'], category_dict['title'], my_dict['rating'], my_dict['location']['display_address'], my_dict['display_phone']]}
                        for key in my_restaurant_dict:
                            url = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(key)
                            name = my_restaurant_dict[key][0]
                            cuisine = my_restaurant_dict[key][1]
                            rating = my_restaurant_dict[key][2]
                            address = my_restaurant_dict[key][3]
                            phone = my_restaurant_dict[key][4]
                            get_business_review(name, cuisine, rating, address, phone, url, headers)


def get_business_review(name, cuisine, rating, address, phone, url, headers):
    print bcolors.FAIL + 'Name: {}'.format(name) + bcolors.ENDC
    print 'Cuisine: {}\nRating: {}\nAddress: {}\nPhone: {}\nReview Excerpts:'.format(cuisine, rating, ','.join(address), phone)
    r = requests.request('GET', url, headers=headers)
    data_dict = r.json()
    for k, v in data_dict.items():
        if isinstance(v, list):
            my_list = v
            for x in my_list:
                if isinstance(x, dict):
                    print '{}\n'.format(x['text'])


def main():
    parser = argparse.ArgumentParser(description="Search yelp for restaurant ratings")
    parser.add_argument("location", help="Restaurant location")
    parser.add_argument("-c", "--category", help="Restaurant category - e.g. Italian, Chinese, etc")
    parser.add_argument("-n", "--name", help="Search for specific restaurant")
    args = parser.parse_args()
    
    token = 'V9hGDtp3hZ37M4Sy3wOikgKGXdYE58li5MSPPiS7OD4HvR6V_hFsQma73dF6_7-sEioBUKN2X-D6R1X_PziAAIGOt9FjMfBZRzLKw-RmggO0tPJlT5QlHTAj0JoNXHYx'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    broad_search = {'location': args.location, 'term': 'restaurants', 'categories': args.category}
    single_search = {'term': args.name, 'location': args.location}
    url = 'https://api.yelp.com/v3/businesses/search'

    if args.name:
        get_business_id(url, headers, single_search)
    else:
        get_business_id(url, headers, broad_search)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

