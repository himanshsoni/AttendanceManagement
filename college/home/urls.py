from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about', views.about,name='about'),
    path('student', views.student,name='student'),
    path('faculty', views.faculty,name='faculty'),
    path('login', views.loginUser,name='loginUser'),
    path('logout', views.logoutUser,name='loginUser'),
]