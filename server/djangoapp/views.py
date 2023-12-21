from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealers_by_id, get_dealers_by_state, get_dealer_reviews_from_cf, post_request, get_request



# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-central1-sublime-habitat-406606.cloudfunctions.net/function-get-all"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

def get_dealer_by(request, **kwargs):
    dealer_id = kwargs.get('dealer_id')
    dealers_state = kwargs.get('dealer_state')
    url = "https://us-central1-sublime-habitat-406606.cloudfunctions.net/function-get-all"
    if dealer_id:
        dealer = get_dealers_by_id(url, dealer_id=dealer_id)
        return HttpResponse(dealer)
    elif dealers_state:
        dealers = get_dealers_by_state(url, dealer_state=dealers_state)
        return HttpResponse(dealers)
    else:
        return HttpResponse("there is a problem in dealerI_id / dealers_state in get_dealer_by")

        


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, **kwargs):
    dealer_id = kwargs.get('dealer_id')
    url = "https://us-central1-sublime-habitat-406606.cloudfunctions.net/get_reviews"
    results = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
    string = ' '.join([reviewer.review + " and the emotion is : " + str(reviewer.sentiment) for reviewer in results])
    return HttpResponse(string)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, **kwargs):
    dealer_id = kwargs.get('dealer_id')
    the_review = kwargs.get('review')
    url = "https://us-central1-sublime-habitat-406606.cloudfunctions.net/add_reviews"
    get_url = "https://us-central1-sublime-habitat-406606.cloudfunctions.net/get_reviews"

    authenticate = get_request(get_url, dealer_id=dealer_id)
    if authenticate is not {}:
        review = dict()
        review['purchase_date'] = datetime.utcnow().isoformat()
        review['dealership']= dealer_id
        review['reivew'] = the_review
        json_payload = dict()
        json_payload['review'] = review
        json_payload = json.dumps(json_payload)
        new_json = json.loads(json_payload)
        json_result = post_request(url,json=new_json, dealer_id=dealer_id)
        return HttpResponse(json_result)
    else:
        return "you are not authenticated, please try again with another username or password"


        


