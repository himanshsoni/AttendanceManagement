from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login


# Create your views here.
def loginpage(request):
#    #return HttpResponse('This is my homepage')
        return redirect("/login")

#def demo(request):
 #  if request.user_type == "admin":
  #       return render(request,'about.html')
   #if user_type == "student":
    #return HttpResponse('This is my student')
    #    return render(request,'student.html')
   #if request.user_type == "faculty":
    #return HttpResponse('This is my faculty')             
    #     return render(request,'faculty.html')
     
        
def about(request):
    #return HttpResponse('This is my about')
    return render(request,'about.html')
def student(request):
    #return HttpResponse('This is my student')
    context = {'username' :request.user.get_full_name()}
    return render(request,'student.html',context)
def faculty(request):
    #return HttpResponse('This is my faculty')             
    return render(request,'faculty.html')
def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        context={'username':username}
        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            if user_type == "admin":
                #login(request, user)
                return redirect("/admin",)
            elif user_type == "faculty":
                login(request, user)
                return redirect("/faculty")
            elif user_type == "student":
                login(request, user)
                return redirect("/student")

        else:
            context={'error':'Wrong username or password !'}
            return render(request, 'login.html',context)

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")