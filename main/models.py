from django.db import models

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

# Create your models here.
