from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from homeapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('loginn',views.loginn,name='loginn'),
    path('studentlogin',views.studentlogin,name='studentlogin'),
    path('companylogin',views.companylogin,name='companylogin'),
    path('companyreg',views.companyreg,name='companyreg'),
    path('studentreg',views.studentreg,name='studentreg'),
    path('compindex',views.compindex,name='compindex'),
    path('studindex',views.studindex,name='studindex'),
    path('logoutt',views.logoutt,name="logoutt"),
    path('compreq',views.compreq,name="compreq"),
    path('viewstudents',views.viewstudents,name="viewstudents"),
    path('recruitedstudents',views.recruitedstudents,name="recruitedstudents"),
    path('company',views.company,name="company"),
    
]