from django.shortcuts import render, redirect
from django.db.models import Q # search multiple field at once
from .forms import AssignmentForm, BaseAssignmentFormSet, AssignmentSetForm, AssignmentFormSet
from .models import Assignment, Unit, AssignmentSet

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
def unit_detail(request, unit_id):
    unit = Unit.objects.get(id=unit_id)

    assignment_set = unit.assignment_set.first()

    if not assignment_set:
        assignment_set = AssignmentSet.objects.create(
            unit=unit,
            title="Default Set"
        )

    # ✔ title form
    set_form = AssignmentSetForm(request.POST or None, instance=assignment_set)

    # ✔ assignment formset
    formset = AssignmentFormSet(
        request.POST or None,
        queryset=assignment_set.assignments.all()
    )

    if request.method == "POST":

        # save title
        if set_form.is_valid():
            set_form.save()

        # save assignments (NO delete logic)
        if formset.is_valid():
            instances = formset.save(commit=False)

            for obj in instances:
                obj.assignment_set = assignment_set
                obj.save()

        return redirect('unit_detail', unit_id=unit.id)

    return render(request, "something/unit.html", {
        "unit": unit,
        "assignment_set": assignment_set,
        "formset": formset,
        "set_form": set_form
    })
def details(request, unit_id, set_id):
    unit = Unit.objects.get(id=unit_id)
    assignment_set = AssignmentSet.objects.get(id=set_id, unit=unit)

    formset = AssignmentFormSet(
        request.POST or None,
        queryset=assignment_set.assignments.all()
    )

    if request.method == "POST":
        if formset.is_valid():
            instances = formset.save(commit=False)

            for obj in instances:
                obj.assignment_set = assignment_set
                obj.save()

            return redirect('details', unit_id=unit.id, set_id=assignment_set.id)

    return render(request, 'something/originaltemplates.html', {
        'unit': unit,
        'assignment_set': assignment_set,
        'formset': formset
    })
# Create your views here.

# http://127.0.0.1:8000/