import time
import requests
from pprintpp import pprint
from genson import SchemaBuilder
from datetime import datetime

# Data is being queried from OpenAQ (open air-quality data)
URL_MEASUREMENTS = "https://api.openaq.org/v2/measurements"
URL_LOCATIONS = "https://api.openaq.org/v2/locations"
URL_LATEST = "https://api.openaq.org/v2/latest"

def make_request(url, params):
    r = requests.get(url, params=params)
    # If no valid response from the api print error and retry
    while not r:
        print("API did not return 200 response")
        time.sleep(5)
        r.requests.get(url, params=params)
    return r

payload = {}
# retrieving all data for the measurements
res_measure = make_request(URL_MEASUREMENTS, payload)
json_measure = res_measure.json()
# print(res.json())

# issue here is that it is hard to read the structure of the data itself, so how about we try prettyprint

# retrieving all data for locations
res_loc = make_request(URL_LOCATIONS, {})
json_loc = res_loc.json()
# print(json_res)
# pprint(json_res)

# prettyprint helped us decipher the complicated nested structure a tad bit, but since the output is so enormous,
# it is still hard for us to understand what is happening. What we want is referred to as the JSON schema
# (a shallow structure)

# we use genson to solve this issue
builder = SchemaBuilder()
builder.add_object(json_loc)
pprint(builder.to_schema())

builder2 = SchemaBuilder()
builder2.add_object(json_measure)
pprint(builder2.to_schema())

# A set of python generator functions that help me determine dictionary keys and list indices that lead to the value I would like.

def find_key(obj, key):
    if isinstance(obj, dict):
        yield from iter_dict(obj, key, [])
    elif isinstance(obj, list):
        yield from iter_list(obj, key, [])


def iter_dict(d, key, indices):
    for k, v in d.items():
        if k == key:
            yield indices + [k], v
        if isinstance(v, dict):
            yield from iter_dict(v, key, indices + [k])
        elif isinstance(v, list):
            yield from iter_list(v, key, indices + [k])


def iter_list(seq, key, indices):
    for k, v in enumerate(seq):
        if isinstance(v, dict):
            yield from iter_dict(v, key, indices + [k])
        elif isinstance(v, list):
            yield from iter_list(v, key, indices + [k])


#for t in find_key(json_loc, 'country'):
#    print(t)


# TODO: retrieving all the country locations within the JSON
def obtain_freq(obj, key):
    """
    now we want to store the frequency of each country appearing, let's say for instance.
    {"US": 82, "BR": 3}
    """
    freq = dict()
    for t in find_key(obj, key):
        if t[1] in freq:
            freq[t[1]] += 1
        else:
            freq[t[1]] = 1
    return freq


# print(obtain_freq(json_loc, 'country'))
print(obtain_freq(json_loc, 'sensorType'))
for t in find_key(json_loc, 'name'):
    print(t)
# print(obtain_freq(json_loc, 'name'))

# To get the first path and value that matches this key


seq, val = next(find_key(json_loc, 'name'))
print('seq:', seq, 'val:', val)
print()

print('PARAMETERS FROM MEASURE: ', obtain_freq(json_measure, 'parameter'))
print('COUNTRY MEASURE DICT: ', obtain_freq(json_measure, 'country'))

print('CITY MEASURE DICT: ')
pprint(obtain_freq(json_measure, 'city'))

#analyzing the timestamps of the data queried from the API
for t in find_key(json_measure, 'utc'):
    timestamp = datetime.fromisoformat(t[1]) #,'%Y-%m-%dT%H:%M:%S.%fZ')
    print(timestamp)


# We now see from the output that there are 100 results returned, a lot of the cases involve the US!
# The API response is paginated, there are more than 100 records that should be returned.

# issue here is that we are only getting 100 records everytime we do an API call. This is obviously not our intended
# goal, rather it is to get all the data! With that in mind:
def iterate_request(url, payload):
    r = make_request(url, payload)
    req_json = r.json()
    metadata = req_json['meta']
    data = req_json['results']

    num_pages = int(metadata['found']/metadata['limit']) + 1

    num_pages = min(20, num_pages)

    for i in range(2, num_pages+1):
        payload['page'] = i
        r = make_request(url, payload)
        print("Requesting page " + str(i) + " of " + str(num_pages) + " from the API")
        data = data + r.json()['results']
    return data

json_measure_full = iterate_request(URL_MEASUREMENTS, {'limit': 1000})

pprint(obtain_freq(json_measure_full, 'utc'))
print(datetime.utcnow())

json_latest_full = iterate_request(URL_LATEST, {'limit': 1000})
pprint(obtain_freq(json_latest_full, 'lastUpdated'))
print(datetime.utcnow())

# Interesting transition to Pub/Sub Model for the API found here:
# https://openaq.medium.com/get-faster-access-to-real-time-air-quality-data-from-around-the-world-c6f9793d5242

'''
 To account for this, I'll need to build an HTTP endpoint to receive the POST requests from Amazon SNS. 
 I'll fidget around with TileJSON in this API first. I'm curious as to how it functions and how it can 
 transpose to a map.
'''

