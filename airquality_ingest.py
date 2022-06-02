
import time
import requests

#Data is being queried from OpenAQ (open air-quality data)
URL_MEASUREMENTS = "https://api.openaq.org/v2/measurements"

def make_request(url, params):
    r = requests.get(url, params=params)
    # If no valid response from the api print error and retry
    while not r:
        print("API did not return 200 response")
        time.sleep(5)
        r.requests.get(url, params=params)
    return r

payload = {}
res = make_request(URL_MEASUREMENTS, payload)
print(res.json())

