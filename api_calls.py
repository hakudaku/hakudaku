#!/Users/vineetbhatia/ENV/bin/python -tt
import json 
import requests
import urllib2 

def out():
  ...

def main():
  client_id = '5fZGdNwU7bZoPZghsGETXQ'
  client_secret = 'yoJQyUoRu5HW4mAXM9c4rnnGaYMvcDYCPZDjzNOEK1oFJZvLWDOfztlklbLZJq6p'
  token = 'Vs_KM7RKRLX_IpTekf4eBQzJbLcU9v29LD61yS953qzzuWt_nugEjnd686sEPpVSh4AYc9qNyNjf6aSc-UZ7I3b94CUTWnYx'
  
  args = sys.argv[1:]
  usage = ('yelp_api.py [x]\n'
           'Example: yelp_api.py x')
  if not args or len(args) < 1:
    print usage
    sys.exit(1)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

