from django.contrib import messages
from django.db.models.fields import DateField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib.auth.models import User
from homeapp.models import Company, Student
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.


def index(request):
    logout(request)
    return render(request, 'index.html')


def loginn(request):
    logout(request)
    return render(request, 'loginn.html')


def studentlogin(request):        
    return render(request, 'studentlogin.html')

def companylogin(request):
    return render(request, 'companylogin.html')


def companyreg(request):
    if request.method == "POST":
        companyname = request.POST.get("companyname")
        companyid = request.POST.get("companyid")
        password = request.POST.get("password")

        if Company.objects.all().filter(companyid=companyid).exists():
            messages.warning(request, 'Company already exists')
            return redirect(companyreg)
        
        myComp = Company(companyname=companyname, companyid=companyid)
        myComp.save()
        user = User.objects.create_user(companyid, '', password)
        user.save()
        messages.success(request, 'You have been registered.')

    return render(request, 'companyreg.html')


def studentreg(request):
    if request.method == "POST":
        studentname = request.POST.get("studentname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        branch = request.POST.get("branch")
        semester = request.POST.get("semester")
        percentage = request.POST.get("percentage")
        password = request.POST.get("password")

        if Student.objects.all().filter(username=username).exists():
            messages.warning(request, 'Student already exists')
            return redirect(studentreg)

        myStud = Student(studentname=studentname,username=username,email=email,branch=branch,semester=semester,percentage=percentage)
        myStud.save()

        user = User.objects.create_user(username, email, password)
        user.save()

        messages.success(request, 'You have been registered.')

    return render(request, 'studentreg.html')

def compindex(request):
    if request.method == "POST":
        companyid = request.POST.get("companyid")
        password = request.POST.get("password")

        obj=Company.objects.all().filter(companyid=companyid)
        if len(obj)==1:
            user = authenticate(username=companyid, password=password)
            if user is not None:
                login(request,user)
                return render(request,'company/compindex.html',{'comp':obj[0]})
            else:
                messages.warning(request, 'Invalid credentials')
                return redirect('/companylogin')
        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('/companylogin')

    if request.user.is_authenticated:
        obj=Company.objects.all().filter(companyid=request.user.username)
        if len(obj)==1:
            return render(request,'company/compindex.html',{'comp':obj[0]})
        else:
            return redirect('/companylogin')
    else:
        return redirect('/companylogin')

def studindex(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        obj=Student.objects.all().filter(username=username)
        if len(obj)==1:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                if obj[0].recruited=='':
                    rec=0
                else:
                    rec=1
                return render(request,'student/studindex.html',{'studset':obj[0],'rec':rec})
            else:
                messages.warning(request, 'Invalid credentials')
                return redirect('/studentlogin')
        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('/studentlogin')

    if request.user.is_authenticated:
        obj=Student.objects.all().filter(username=request.user.username)
        if len(obj)==1:
            if obj[0].recruited=='':
                rec=0
            else:
                rec=1
            return render(request,'student/studindex.html',{'studset':obj[0],'rec':rec})
        else:
            return redirect('/studentlogin')
    else:
        return redirect('/studentlogin')

def logoutt(request):
    logout(request)
    return redirect('/')

def compreq(request):
    if request.method == "POST":
        minpercentage = request.POST.get("minpercentage")
        branch = request.POST.get("branch")
        minsemester = request.POST.get("minsemester")
        interviewdate = request.POST.get("interviewdate")
        interviewtime = request.POST.get("interviewtime")
        obj=Company.objects.all().filter(companyid=request.user.username)[0]
        obj.minpercentage=minpercentage
        obj.branch=branch
        obj.minsemester=minsemester
        obj.interviewdate=interviewdate
        obj.interviewtime=interviewtime
        obj.save()

    return redirect('/compindex')   

def viewstudents(request):
    if request.method=="POST":
        username=request.POST.get("username")
        obj=Student.objects.all().filter(username=username)
        if(len(obj)==1):
            studobj=obj[0]
            studobj.recruited=request.user.username
            studobj.save()
        return redirect('/viewstudents')

    compobj=Company.objects.all().filter(companyid=request.user.username)[0]
    studset=Student.objects.all().filter(percentage__gte=compobj.minpercentage,branch=compobj.branch,semester__gte=compobj.minsemester,recruited='')
    return render(request,'company/viewstudents.html',{'studset':studset})

    
def recruitedstudents(request):
    if request.method=="POST":
        username=request.POST.get("username")
        obj=Student.objects.all().filter(username=username)
        if(len(obj)==1):
            studobj=obj[0]
            studobj.recruited=''
            studobj.save()
        return redirect('/recruitedstudents')

    studset=Student.objects.all().filter(recruited=request.user.username)
    return render(request,'company/recruitedstudents.html',{'studset':studset})

def company(request):
    studobj=Student.objects.all().filter(username=request.user.username)[0]
    compset=Company.objects.all().filter(minpercentage__lte=studobj.percentage,branch=studobj.branch,minsemester__lte=studobj.semester)
    return render(request,'student/company.html',{'compset':compset})