from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login


# Create your views here.
def home(request):
    #return HttpResponse('This is my homepage')
    #context={'name':'Himansh','course':'Django','instructor':'Harry'}
    if request.user.is_anonymous:
        return redirect("/login") 
    return render(request,'home.html')
def about(request):
    #return HttpResponse('This is my about')
    return render(request,'about.html')
def student(request):
    #return HttpResponse('This is my student')
    return render(request,'student.html')
def faculty(request):
    #return HttpResponse('This is my faculty')             
    return render(request,'faculty.html')
def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")