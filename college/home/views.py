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


#Database Connection
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
    subjects = ['os','cpp','toc','dbms']
    attendences = {}
    for i in subjects:
        cursor.execute(f"SELECT percentage from {i} where name=\"{request.session['username'].upper()}\";")
        percentage = cursor.fetchall()[0][0]
        attendences[i] = percentage
    print(attendences)
    today = date.today()
    date_column = today.strftime("%B_%d_%Y")
    date_string = today.strftime("%d-%m-%Y")
    context = {'attendences' :attendences,'username':request.session['username'].upper()}
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
            #print(user_type)
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
    request.session['last_subject_taken'] = subject
    ip_date = request.POST['ip_date']
    att = list(request.POST.values())[3:]
    roll = list(request.POST.keys())[3:]
    date_object = datetime.strptime(ip_date,"%Y-%m-%d")
    date_column = date_object.strftime("%B_%d_%Y")
    cursor.execute(f"SELECT total FROM subject_total_attendence WHERE subject = \"{subject}\";")
    total = cursor.fetchall()[0][0]
    cursor.execute(f"SELECT COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{subject}';")
    columns = cursor.fetchall()
    columns = [i[0] for i in columns]
    if date_column not in columns:
        cursor.execute(f"ALTER TABLE {subject} ADD COLUMN {date_column} VARCHAR(1);")
        total += 1
        cursor.execute(f"UPDATE subject_total_attendence SET total={total} WHERE subject = \"{subject}\";")
    for i in range(len(roll)):
        #print(subject,roll[i])
        cursor.execute(f"SELECT present , {date_column} FROM {subject} WHERE roll_no=\'{roll[i]}\';")
        temp = cursor.fetchall()[0]
        print(temp)
        present = temp[0]
        previous_attendence = temp[1]
        if att[i].upper()=='P':
            if previous_attendence =='A' or previous_attendence==None:
                present+=1
            percentage = ((present)/total)*100
            cursor.execute(f"UPDATE {subject} SET {date_column} = '{att[i].upper()}' ,\
            present = {present} , percentage = {percentage}  WHERE roll_no = '{roll[i]}';")
        else:
            percentage = ((present)/total)*100
            cursor.execute(f"UPDATE {subject} SET {date_column} = 'A' ,\
            percentage = {percentage}  WHERE roll_no = '{roll[i]}';")
    mydb.commit()
    return render(request,'attendence_taken.html')
    
def student_download(request):
    cursor.execute("SELECT subject FROM subject_total_attendence;")
    subjects = [i[0] for i in cursor.fetchall()]
    dfs = []
    #print(subjects)
    for subject in subjects:
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{subject}\' ORDER BY ORDINAL_POSITION")
        columns = cursor.fetchall()[4:]
        columns = [i[0] for i in columns]
        col_string = ""
        for i in range(len(columns)):
            if i<len(columns)-1:
                col_string += f"{columns[i]},"
            else:
                col_string += f"{columns[i]}"
        if columns:
            #print("SELECT {} FROM {} WHERE name=\'{}\';".format(col_string,subject,request.session['username']))
            cursor.execute("SELECT {} FROM {} WHERE name=\'{}\';".format(col_string,subject,request.session['username']))
            data = cursor.fetchall()
            dfs.append(pd.DataFrame(data, columns = columns , index=[subject]))
        else:
            dfs.append(pd.DataFrame(data=None , columns = columns , index = [subject]))
    for i in dfs:
        print(i)
    df = pd.concat(dfs)
    df = df.reset_index().rename(columns={'index': 'Subjects'})
    df['Subjects'] = df['Subjects'].str.upper()
    df.fillna("-",inplace=True)
    #print(df.columns)
    #print(df)
    df.to_excel("Download.xlsx",index = False)
    path = "F:\Github\AttendanceManagement\college\Download.xlsx"
    with open(path, 'rb') as pdf:
        data = pdf.read()
        response =  HttpResponse(data, content_type='application/ms-excel charset=utf-8')
        response["Content-Length"] = len(data)
        response['Content-Disposition'] = 'attachment;filename=Attendence-Report.xlsx' 
    #response = FileResponse(open("Download.txt", 'rb'))
    return response
    
def faculty_download(request):
    subject = request.session['last_subject_taken']
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{subject}\' ORDER BY ORDINAL_POSITION")
    columns = cursor.fetchall()
    columns = [i[0] for i in columns]
    cursor.execute(f"SELECT * FROM {subject};")
    data = cursor.fetchall()
    df = pd.DataFrame(data,columns = columns)
    df.columns = df.columns.str.upper()
    print(df)
    df.to_excel("Download.xlsx",index = False)
    path = "F:\Github\AttendanceManagement\college\Download.xlsx"
    with open(path, 'rb') as pdf:
        data = pdf.read()
        response =  HttpResponse(data, content_type='application/ms-excel charset=utf-8')
        response["Content-Length"] = len(data)
        response['Content-Disposition'] = 'attachment;filename=Faculty-Attendence.xlsx' 
    #response = FileResponse(open("Download.txt", 'rb'))
    return response
    
    
