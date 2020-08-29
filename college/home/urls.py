from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.loginpage,name='loginpage'),
    path('about', views.about,name='about'),
    path('download', views.download,name='download'),
    path('studentattendence', views.student_attendence,name='student_attendence'),
    path('facultyattendence', views.faculty_attendence,name='faculty_attendence'),
    path('attendencetaken', views.attendence_taken,name='attendence_taken'),
    path('login', views.loginUser,name='loginUser'),
    path('logout', views.logoutUser,name='logoutUser'),
]
