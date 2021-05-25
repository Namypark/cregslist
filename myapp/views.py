import requests 
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models


BASE_URL = "https://losangeles.craigslist.org/search/?query={}"
IMAGE_BASE_URL = "https://images.craigslist.org/{}_300x300.jpg"
# Create your views here.
def home(request):
    return render(request, 'base.html')

#* this is made for get the search keyed in by the user
#* adding it to the local databse and formatting it into the final url
#* to display a searched item
def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)

    data = response.text
    #parsing the html file to Beautiful soup
    soup = BeautifulSoup(data, features='html.parser')

    #finding the row --> this contains majority of the info we want to scrape
    post_listings  = soup.find_all('li', {'class':'result-row'})
    
    final_postings = []

    #* iterates through the post_listings to find the \
    #* Titles,url,price and image url
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_ = 'result-price'):  
            post_price = post.find(class_= 'result-price').text
        else:
            post_price = "N/A"
        #* Here we are finding all url images 
        #* but if there are no images we used a fixed images
        if post.find(class_='result-image').get('data-ids'):
            post_image_url = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = IMAGE_BASE_URL.format(post_image_url)
        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"
        final_postings.append((post_title, post_url, post_price, post_image_url))

    frontend = {
        'search':search,
        'final_postings':final_postings,
    }
    return render(request,'myapp/new_search.html',frontend)


