from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        
        return HttpResponseRedirect(reverse('djangoapp:index'))

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == 'GET':
        logout(request)

    return HttpResponseRedirect(reverse('djangoapp:index'))

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html')
    elif request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], "", request.POST['password'])
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('djangoapp:index'))

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/f65fcf3d-6503-43a5-956c-c6ccef1a7764/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/f65fcf3d-6503-43a5-956c-c6ccef1a7764/dealership-package/get-review"
        dealer = get_dealer_by_id_from_cf(url, dealer_id)
        return HttpResponse(dealer)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

