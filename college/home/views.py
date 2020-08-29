from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
import random
import pandas as pd
from django.http import FileResponse
from datetime import date,datetime
import MySQLdb as sql
import pandas as pd
from .models import Toc



mydb = sql.connect(user='root',password='aayush',database='second_year')    
cursor = mydb.cursor()




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
def student_attendence(request):
    today = date.today()
    date_column = today.strftime("%B_%d_%Y")
    date_string = today.strftime("%d-%m-%Y")
    cursor.execute(f"SELECT roll_no , name , {date_column} from TOC;")
    table = cursor.fetchall()
    context = {'table' :table,'date':date_string,'username':request.session['username'].upper()}
    return render(request,'student_attendence.html',context)
def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        request.session['username']=username
        user_exist = cursor.execute(f'SELECT user_type FROM users WHERE user=\'{username.upper()}\' and password=\'{password}\';')
        if user_exist:
            user_type = cursor.fetchall()[0][0]
            print(user_type)
            # check if user has entered correct credentials
            #user = authenticate(username=username, password=password)
            # A backend authenticated the credentials
            if user_type == "admin":
                    #login(request, user)
                    return redirect("/admin")
            elif user_type == "faculty":
                    #login(request, user)
                    return redirect("/facultyattendence")
            elif user_type == "student":
                    #login(request, user)
                    return redirect("/studentattendence")

        else:
            context={'error':'Wrong username or password !'}
            return render(request, 'login.html',context)

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

def faculty_attendence(request):
    #print(request.session.values())
    faculty_name = request.session['username'].upper()
    cursor.execute("SELECT roll_no,name from students;")
    table_data = cursor.fetchall()
    cursor.execute(f"SELECT subjects from faculty where name=\'{faculty_name}\';")
    subjects = cursor.fetchall()
    subjects = subjects[0][0].split(',')
    print(subjects)
    #print(table)
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")
    context = {'table' :table_data ,'date':date_string,'username':faculty_name,'subjects':subjects}
    return render(request,'faculty_attendence.html',context)

def attendence_taken(request):
    subject = request.POST['subject']
    ip_date = request.POST['ip_date']
    att = list(request.POST.values())[2:]
    roll = list(request.POST.keys())[2:]
    date_object = datetime.strptime(ip_date,"%Y-%m-%d")
    date_column = date_object.strftime("%B_%d_%Y")
    cursor.execute(f"SELECT COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{subject}';")
    columns = cursor.fetchall()
    columns = [i[0] for i in columns]
    #print(columns)
    if date_column not in columns:
        a = cursor.execute(f"ALTER TABLE {subject} ADD COLUMN {date_column} VARCHAR(1);")
    for i in range(len(roll)):
        if att[i]:
            cursor.execute(f"UPDATE {subject} SET {date_column} = '{att[i].upper()}' WHERE roll_no = '{roll[i]}';")
        else:
            cursor.execute(f"UPDATE {subject} SET {date_column} = 'A' WHERE roll_no = '{roll[i]}';")
    mydb.commit()
    return render(request,'attendence_taken.html')
    
def download(request):
    obj = Toc.objects.all()
    #print(obj.values())
    df = pd.DataFrame(obj.values())
    df.to_excel("Download.xlsx",index = False)
    path = "F:\Github\AttendanceManagement\college\Download.xlsx"
    with open(path, 'rb') as pdf:
        data = pdf.read()
        response =  HttpResponse(data, content_type='application/ms-excel charset=utf-8')
        response["Content-Length"] = len(data)
        response['Content-Disposition'] = 'attachment;filename=Download.xlsx' 
    #response = FileResponse(open("Download.txt", 'rb'))
    return response