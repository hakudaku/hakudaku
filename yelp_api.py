#!/Users/vbhatia/ENV/bin/python -tt
import json 
import requests
import urllib2 

def out(payload, url):
  print payload
  r = requests.request('GET', url, params=payload)
  print r.json()
  

def main():
  #headers = {'content-type': 'application/x-www-form-urlencoded'}
  client_id = '5fZGdNwU7bZoPZghsGETXQ'
  client_secret = 'yoJQyUoRu5HW4mAXM9c4rnnGaYMvcDYCPZDjzNOEK1oFJZvLWDOfztlklbLZJq6p'
  token = 'PBygzlZJDF6ikffoak_QfwtOxxHkZCo-Vs_KM7RKRLX_IpTekf4eBQzJbLcU9v29LD61yS953qzzuWt_nugEjnd686sEPpVSh4AYc9qNyNjf6aSc-UZ7I3b94CUTWnYx'
  payload = {
        'Authorization': 'Bearer %s' % token,
    }
  url = 'https://api.yelp.com/v3/businesses/spalti-palo-alto'
  out(payload, url)
  

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

