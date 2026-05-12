from django.shortcuts import render, redirect
from django.db.models import Q # search multiple field at once
from .forms import AssignmentForm, BaseAssignmentFormSet, AssignmentSetForm, AssignmentFormSet, UploadForm
from .models import Assignment, Unit, AssignmentSet, Upload
from django.shortcuts import render, get_object_or_404  

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

    # title form
    set_form = AssignmentSetForm(request.POST or None)

    # assignment formset
    formset = AssignmentFormSet(
        request.POST or None,
        queryset=Assignment.objects.none()
    )

    if request.method == "POST":

        if set_form.is_valid() and formset.is_valid():

            # create AssignmentSet after submit
            assignment_set = set_form.save(commit=False)
            assignment_set.unit = unit
            assignment_set.save()

            # save assignments
            instances = formset.save(commit=False)

            for obj in instances:
                obj.assignment_set = assignment_set
                obj.save()

            return redirect(
                'unitlist',
                set_id=assignment_set.id
            )

    return render(request, 'something/unit.html', {
        'unit': unit,
        'set_form': set_form,
        'formset': formset,
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




def unitlist(request, set_id):

    assignment_set = get_object_or_404(AssignmentSet, id=set_id)
    unit = assignment_set.unit

    set_form = AssignmentSetForm(
        request.POST or None,
        instance=assignment_set
    )

    formset = AssignmentFormSet(
        request.POST or None,
        queryset=assignment_set.assignments.all()
    )

    if request.method == "POST":

        if set_form.is_valid() and formset.is_valid():

            set_form.save()

            instances = formset.save(commit=False)

            for obj in instances:
                obj.assignment_set = assignment_set
                obj.save()

            return redirect('outline_detail', set_id=assignment_set.id)

    return render(request, 'something/unitlist.html', {
        'unit': unit,
        'assignment_set': assignment_set,
        'set_form': set_form,
        'formset': formset,
    })

def upload_file(request):
    form = UploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('file_page')

    files = Upload.objects.all()

    return render(request, 'something/upload_file.html', {
        'form': form,
        'files': files
    })
# Create your views here.

# http://127.0.0.1:8000/
