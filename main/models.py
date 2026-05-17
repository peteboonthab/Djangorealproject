from django.db import models
from django.core.validators import RegexValidator

class Unit(models.Model):
    unit_name = models.CharField(max_length = 50)
    unit_goal = models.CharField(max_length = 50)
    unit_description = models.CharField(max_length = 50)

class AssignmentSet(models.Model):
    title = models.CharField(max_length = 50)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="assignment_set", null=True, blank=True)


class Assignment(models.Model):
    assignment_name = models.CharField(max_length = 20)
    assignment_weight = models.IntegerField() # stored number in database
    assignment_set = models.ForeignKey(AssignmentSet, on_delete=models.CASCADE, related_name="assignments", null=True, blank=True)


    def __str__(self):
        return self.assignment_name
class Upload(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to="resources/")

class Signin(models.Model):
    role_choices = ['student','student'
                    'teacher','teacher']
    user = models.CharField(max_length=20, unique=True)
    password = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^(?=.*@).{10,20}$',
                message="Enter a valid registration number in the format ABCDEFG123@",
                code="invalid_registration",
            ),
        ],
    )
    role = models.CharField(max_length=10, default = 'student')

    def __str__(self):
        return self.user

# Create your models here.
