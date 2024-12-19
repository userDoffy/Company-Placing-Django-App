from datetime import date, timezone
import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Company(models.Model):
    companyname=models.CharField(max_length=122)
    companyid=models.CharField(max_length=122)

    # company requirements
    minpercentage=models.DecimalField(decimal_places=2,max_digits=10,default=35)
    branch=models.CharField(max_length=122,default='')
    minsemester=models.IntegerField(default=1)
    interviewdate=models.DateField(default=date.today)
    interviewtime=models.TimeField(default=timezone.now)
    
    def __str__(self) :
        return self.companyname

class Student(models.Model):
    username=models.CharField(max_length=122)
    studentname=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    branch=models.CharField(max_length=122)
    semester=models.IntegerField()
    percentage=models.DecimalField(decimal_places=2,max_digits=10)
    recruited=models.CharField(max_length=122,default='')
    
    def __str__(self) :
        return self.studentname
    