import time
import requests
from pprintpp import pprint
from genson import SchemaBuilder

# Data is being queried from OpenAQ (open air-quality data)
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
# retrieving all data for the measurements
res = make_request(URL_MEASUREMENTS, payload)
# print(res.json())

# issue here is that it is hard to read the structure of the data itself, so how about we try prettyprint

# retrieving all data for locations
res = make_request(URL_LOCATIONS, {})
json_res = res.json()
# print(json_res)
# pprint(json_res)

# prettyprint helped us decipher the complicated nested structure a tad bit, but since the output is so enormous,
# it is still hard for us to understand what is happening. What we want is referred to as the JSON schema
# (a shallow structure)

# we use genson to solve this issue
builder = SchemaBuilder()
builder.add_object(json_res)
# pprint(builder.to_schema())


# issue here is that we are only getting 100 records everytime we do an API call. This is obviously not our intended
# goal, rather it is to get all the data!



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


for t in find_key(json_res, 'country'):
    print(t)

# We now see from the output that there are 100 results returned, a lot of the cases involve the US!

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


print(obtain_freq(json_res, 'country'))
