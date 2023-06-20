import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if 'api_key' in kwargs:
            # params = dict()
            # params["text"] = kwargs["text"]
            # params["version"] = kwargs["version"]
            # params["features"] = kwargs["features"]
            # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', kwargs.get('api_key')))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
        response = {
            'status_code': 500,
            'text': 'Server error'
        }
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_from_cf(dealerId):
    json_result = get_request('https://us-south.functions.appdomain.cloud/api/v1/web/f65fcf3d-6503-43a5-956c-c6ccef1a7764/dealership-package/get-dealership', dealer_id=dealerId)
    return json_result

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    json_result = get_request(url, dealerId=dealerId)
    result = []
    for doc in json_result:
        sentiment = analyze_review_sentiments(doc['review'])
        review_obj = DealerReview(
            dealership = doc['dealership'],
            id = doc['_id'],
            name = doc['name'],
            purchase = doc['purchase'],
            review = doc['review'],
            purchase_date = doc.get('purchase_date', ''),
            car_make = doc.get('car_make', ''),
            car_model = doc.get('car_model', ''),
            car_year = doc.get('car_year', ''),
            sentiment = sentiment)
        result.append(review_obj)
    return result

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    authenticator = IAMAuthenticator('q0gjsWC81P0Q7h3LK6swMGTsRC1ZGwe-U_fFk3rxH72-')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/c4d89b24-007a-4e2d-a921-f92372e157c0')

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(document=True)),
        language='en'
    ).get_result()
    
    return response['sentiment']['document']['label']