from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.loginpage,name='loginpage'),
    path('about', views.about,name='about'),
    path('student', views.student,name='student'),
    path('faculty', views.faculty,name='faculty'),
    path('attendence', views.attendence,name='attendence'),
    path('login', views.loginUser,name='loginUser'),
    path('logout', views.logoutUser,name='logoutUser'),
]