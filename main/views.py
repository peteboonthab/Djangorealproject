from django.shortcuts import render
from .models import Unit
from django.db.models import Q # search multiple field at once
from .forms import AssignmentForm
from .models import Assignment 

def index(request):
    units = Unit.objects.all()
    return render (request,"something/unit.html",{'units':units})

def search_unit(request):


    if request.method == "GET": 
        query = request.GET.get('q') #get the value of parameter 'q' from URL and stored it in variable query 

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

def creation(request):
    form = AssignmentForm()
    assignments = Assignment.objects.all()
    context = {
        'form':form,
        'assignments':assignments, }

    if request.method == "POST" :
        if "save" in request.POST:
            pk = request.POST.get("save")
            if not pk:
                form = AssignmentForm(request.POST)
            else:
                assignment = Assignment.objects.get(id=pk)
                form = AssignmentForm(request.POST, instance=assignment)
            form.save()
            form = AssignmentForm()
        elif "delete" in request.POST:
            pk = request.POST.get("delete")
            assignment = Assignment.objects.get(id=pk)
            assignment.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            assignment = Assignment.objects.get(id=pk)
            form = AssignmentForm(instance=assignment)
            
    context['form'] = form
    return render(request, 'something/assignment.html', context)


# Create your views here.

# http://127.0.0.1:8000/