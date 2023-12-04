from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

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
    path("emergency/<int:service_id>/", views.serviceprofile, name="serviceprofile"),
    path("report/", views.report, name="report"),
    path("", views.register, name="register"),
    path("location/", views.location, name="location"),
    path("criminal/", views.criminal, name="criminal"),
    path("criminal/<int:criminal_id>/", views.criminalprofile, name="criminalprofile"),
    path("userprofile/", views.userprofile, name="userprofile"),
    path('logout/', LogoutView.as_view(next_page='http://127.0.0.1:8000/loginpage/'), name='logout'),
    path('send_location/', views.send_location, name='send_location'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
