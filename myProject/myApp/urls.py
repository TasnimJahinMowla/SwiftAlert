from django.contrib import admin
from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

app_name = 'myApp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", views.home, name="home"),
    path("loginpage/", views.loginpage, name="loginpage"),
    path("navigation_bar/", views.navigation_bar, name="navigation_bar"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("notification/", views.notification, name="notification"),
    path("emergency/", views.emergency, name="emergency"),
    path("report/", views.report, name="report"),
    path("", views.register, name="register"),
]
