from django.shortcuts import render
#from django.http import HttpResponse
from listings.models import Listing

# Create your views here.
def index(request):
    #print(request, request.path)
    # content = [{
    #     'anything': 'something speical',
    #     'number' : '1234'
    # }]
    listings = Listing.objects.all()
    content = {
        "listings" : listings
    }
    return render(request,'pages/index.html', content)

def about(request):
    #return HttpResponse('<h1>About</h1>')
    #print(request, request.path)
    return render(request,'pages/about.html')