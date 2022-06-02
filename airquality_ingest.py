
import time
import requests
from pprintpp import pprint
from genson import SchemaBuilder

#Data is being queried from OpenAQ (open air-quality data)
URL_MEASUREMENTS = "https://api.openaq.org/v2/measurements"
URL_LOCATIONS = "https://api.openaq.org/v2/locations"

def make_request(url, params):
    r = requests.get(url, params=params)
    # If no valid response from the api print error and retry
    while not r:
        print("API did not return 200 response")
        time.sleep(5)
        r.requests.get(url, params=params)
    return r

payload = {}
#retrieving all data for the measurements
res = make_request(URL_MEASUREMENTS, payload)
#print(res.json())

#issue here is that it is hard to read the structure of the data itself, so how about we try prettyprint

#retrieving all data for locations
res = make_request(URL_LOCATIONS, {})
json_res = res.json()
#print(json_res)
#pprint(json_res)

#prettyprint helped us decipher the complicated nested structure a tad bit, but since the output is so enormous,
#it is still hard for us to understand what is happening. What we want is referred to as the JSON schema (a shallow structure)

#we use genson to solve this issue

builder = SchemaBuilder()
builder.add_object(json_res)
pprint(builder.to_schema())

# retrieving all the country locations.






