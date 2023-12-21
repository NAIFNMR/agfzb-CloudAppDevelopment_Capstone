import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get('api_key')
    try:
        if api_key:
            params = dict()
            params['text'] = kwargs.get('text')
            params['version'] = kwargs.get('version')
            params['features'] = kwargs.get('features')
            params['return_analyzed_text'] = kwargs.get('return_analyzed_text')
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey',api_key))
        else:
        # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    assert response.status_code == 200    
    # json_data = json.loads(response.text)
    return response

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealers_by_id(url, **kwargs):
    json_result = get_request(url)
    dealer_id = kwargs.get("dealer_id")
    if dealer_id and json_result:
        dealer_new = json_result['dealerships']
        for dealer_doc in dealer_new:
            if dealer_doc['id'] == dealer_id:
                dealer_object = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
                return dealer_object
    else:
        return "there is a poblem in dealer_id / json_result"
    

def get_dealers_by_state(url, **kwargs):
    result = []
    json_result = get_request(url)
    dealers_state = kwargs.get('dealer_state')
    if dealers_state and json_result:
        dealer_new = json_result['dealerships']
        for dealer_doc in dealer_new:
            if dealer_doc['state'] == dealers_state:
                dealer_object = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
                result.append(dealer_object)
        return result
    else:
        return "there is a poblem in dealer_state / json_result"


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    result = []
    json_result = get_request(url)
    reviews = json_result['reviews']
    dealer_id = kwargs.get('dealer_id')
    if dealer_id and reviews:
        for review in reviews:
            if review['dealership'] == dealer_id:
                dealer_review = DealerReview(dealership=review['dealership'], name=review['name'], purchase=review['purchase'], review=review['review'], purchase_date=review['purchase_date'], car_make=review['car_make'], car_model=review['car_model'], car_year=review['car_year'], sentiment="default", id=review['id'])
                # dealer_review.sentiemnts = analyze_review_sentiments(text=dealer_review.review, features = "emotion", version="2022-04-07", return_analyzed_text=True)
                dealer_review.sentiment = analyze_review_sentiments(text=dealer_review.review)
                print(dealer_review.sentiment)
                result.append(dealer_review)
        return result 
    else:
        return "there is a problem in dealer_id / reviews all in get_dealer_reviews-from_cf"




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(**kwargs):
        api_key = "_wfMGclbRkf5iPIHqSL_AeVVLnCx6oEH7Snv8bU4Oe7-"
        new_url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/74ade9c4-ed58-4c1c-b770-5924d45f7d4c/v1/analyze?version=2019-07-12"
        text = kwargs.get('text')
        result = get_request(new_url,text=text, api_key=api_key, features = "emotion", version="2022-04-07", return_analyzed_text=True)
        if result:
            return result
        else:
            return "there is a problem in result in anayze review sentiemnts() "


def post_request(url, **kwargs):
    json_payload = kwargs.get('json')
    if json_payload:
        try:
            print('00000000000000000')
            print(json_payload)
            response = requests.post(url,headers={"Content-Type":"application/json"},json=json_payload)
        except:
            print('there is a problem in json_payload in post_request')
    assert response.status_code == 200
    response_one = json.dumps(response.text)
    json_final = json.loads(response_one)
    return json_final