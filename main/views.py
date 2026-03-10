from django.shortcuts import render
from .models import Unit
from django.db.models import Q # search multiple field at once

def index(request):
    units = Unit.objects.all()
    return render (request,"something/unit.html",{'units':units})

def search_unit(request):


    if request.method == "GET": #GET mean the data go into URL
        query = request.GET.get('q') #get the value of parameter 'q' from database and stored it in variable query 

        if query: #checking if query has value or not
            lookups = Q(unit_name__icontains=query) #Get record that contained value in the specific colump of database --> Q at the front allowed multiple search which can include unit descirption and achievemnet (put | between each conditoin)
            results = Unit.objects.filter(lookups) #Search for which database is true according to the query variable and convert them into lterable (something that can be loop through)
        else:
            results = Unit.objects.all()

    context = {
        'results': results,  #create a dictionary named context that send data from view to html

        
        }
    return render(request, "something/searchunit.html", context)

def details(request, unit_id):
    unit = Unit.objects.get(id=unit_id) #find id database that is the same one recieved from URL, use get here because it will get 1 specific row not every row like all()
    return render (request, 'something/originaltemplates.html', {'unit':unit}) #another way of creating dictionary with 'named used in template" : variable from views

# Create your views here.

# http://127.0.0.1:8000/