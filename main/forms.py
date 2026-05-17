from .models import Assignment, AssignmentSet, Upload, Signin
from django import forms 
from django.forms import BaseModelFormSet, modelformset_factory


class AssignmentForm(forms.ModelForm): #ModelForm read model and create field automtcailly 
    class Meta:
        model = Assignment # use assignment model to generate this form
        fields = ['assignment_name','assignment_weight']

class AssignmentSetForm(forms.ModelForm):
    class Meta:
        model = AssignmentSet
        fields = ['title']

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ["title", "file"]

class SigninForm(forms.ModelForm):
    class Meta:
        model = Signin
        fields = ['user','password']

class BaseAssignmentFormSet(BaseModelFormSet):

    def clean(self):
        super().clean()

        total = 0

        for form in self.forms:
            if form.cleaned_data:
                total += form.cleaned_data.get('assignment_weight', 0)

        if total != 100:
            raise forms.ValidationError("Total assignment score must be = 100%, action not save")

AssignmentFormSet = modelformset_factory(
    Assignment,
    form=AssignmentForm,
    formset=BaseAssignmentFormSet,
    max_num=4,
    extra=4







)


