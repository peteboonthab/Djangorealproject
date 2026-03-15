from .models import Assignment
from django import forms 

class AssignmentForm(forms.ModelForm): #ModelForm read model and create field automtcailly 
    class Meta:
        model = Assignment # use assignment model to generate this form
        fields = ['assignment_name','assignment_weight']

