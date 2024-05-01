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
    path("ml_results/", views.ml_results, name="ml_results"),
    path("criminal/<int:criminal_id>/", views.criminalprofile, name="criminalprofile"),
    path("userprofile/", views.userprofile, name="userprofile"),
    path("adminprofile/", views.adminprofile, name="adminprofile"),
    path('logout/', LogoutView.as_view(next_page='http://127.0.0.1:8000/loginpage/'), name='logout'),
    path('send_location/', views.send_location, name='send_location'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path("admin_panel/<str:model_name>/", views.admin_panel_detail, name="admin_panel_detail"),
    path("admin_panel/<str:model_name>/<int:instance_id>/", views.admin_panel_detail_instance, name="admin_panel_detail_instance"),
     path("admin_panel/<str:model_name>/<int:instance_id>/save/", views.admin_panel_save_instance, name="admin_panel_save_instance"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
