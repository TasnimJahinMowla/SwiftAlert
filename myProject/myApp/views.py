from django.db import IntegrityError  
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, ExpressionWrapper, FloatField 
from django.utils import timezone 
from dateutil.parser import parse 
from datetime import datetime
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from geopy.geocoders import Nominatim
from django.apps import apps
from django.forms import modelform_factory
from .forms import get_dynamic_model_form
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import io
import urllib, base64

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password != confirmpassword:
            return JsonResponse({'message': 'Passwords do not match', 'alert_type': 'danger'})
            redirect 

        try:
            if User.objects.get(username=username):
                return JsonResponse({'message': 'Username is taken', 'alert_type': 'warning'})
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=email):
                return JsonResponse({'message': 'Email is taken', 'alert_type': 'warning'})
        except User.DoesNotExist:
            pass

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/loginpage/')

    context = {}
    return render(request, "myApp/register.html", context)




def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if "Login as Admin" checkbox is selected
        login_as_admin = request.POST.get('login_as_admin') == 'on'

        if login_as_admin:
            # Authenticate as an admin user
            admin_user = authenticate(username=username, password=password)
            if admin_user and admin_user.is_staff:
                login(request, admin_user)
                return redirect('http://127.0.0.1:8000/admin_panel/')  # Redirect to admin panel
            else:
                messages.error(request, "Invalid Admin Credentials")
                return redirect('http://127.0.0.1:8000/loginpage/')
        else:
            # Authenticate as a regular user
            myuser = authenticate(username=username, password=password)
            if myuser:
                login(request, myuser)
                return redirect('http://127.0.0.1:8000/home/')
            else:
                messages.error(request, "Invalid Credentials")
                return redirect('http://127.0.0.1:8000/loginpage/')
    context = {}
    return render(request, "myApp/loginpage.html", context)
    
@login_required
def userprofile(request):
    user = request.user

    try:
        profile, created = UserProfile.objects.get_or_create(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    locations = Location.objects.all()

    if request.method == 'POST':
        bio = request.POST.get('message')
        location_id = request.POST.get('location')
        profile_picture = request.FILES.get('profile_picture')

        if not profile:
            # If the profile doesn't exist, create a new one
            new_profile = UserProfile(user=user, bio=bio, location_id=location_id, image=profile_picture)
            new_profile.save()
        else:
            # Update the existing profile
            profile.bio = bio
            profile.location_id = location_id
            if profile_picture:
                profile.image = profile_picture
            profile.save()

        return redirect('myApp:userprofile')

    context = {
        'profile': profile,
        'locations': locations,
    }
    return render(request, "myApp/userprofile.html", context)
@login_required
def adminprofile(request):
    user = request.user

    try:
        profile, created = UserProfile.objects.get_or_create(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    locations = Location.objects.all()

    if request.method == 'POST':
        bio = request.POST.get('message')
        location_id = request.POST.get('location')
        profile_picture = request.FILES.get('profile_picture')

        if not profile:
            # If the profile doesn't exist, create a new one
            new_profile = UserProfile(user=user, bio=bio, location_id=location_id, image=profile_picture)
            new_profile.save()
        else:
            # Update the existing profile
            profile.bio = bio
            profile.location_id = location_id
            if profile_picture:
                profile.image = profile_picture
            profile.save()

        return redirect('myApp:userprofile')

    context = {
        'profile': profile,
        'locations': locations,
    }
    return render(request, "myApp/adminprofile.html", context)

@login_required
def navigation_bar(request):
    context={}
    return render(request, "myApp/navigation_bar.html")
    
@login_required
def about(request):
    context={}
    return render(request, "myApp/about.html")

@login_required
def services(request):
    context={}
    return render(request, "myApp/services.html")

@login_required
def contact(request):
    context={}
    return render(request, "myApp/contact.html")

@login_required
def notification(request):
    user = request.user
    user_profile = user.userprofile  # Assuming you have a user profile associated with each user

    # Filter notifications for the logged-in user, ordered by timestamp (latest first)
    notifications = user_profile.notifications.all().order_by('-timestamp')

    context = {'notifications': notifications}
    return render(request, "myApp/notification.html", context)

@login_required
def home(request):
    context={}
    return render(request, "myApp/home.html")

@login_required
def areas(request):
    context={}
    return render(request, "myApp/areas.html")

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='home')  # Redirect to 'home' if not an admin
def admin_panel(request):
    models = apps.get_app_config('myApp').get_models()
    model_names = [model._meta.verbose_name for model in models]
    context = {'model_names': model_names}
    return render(request, "myApp/admin_panel.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='home')  # Redirect to 'home' if not an admin
def admin_panel_detail(request, model_name):
    app_config = apps.get_app_config('myApp')
    model = app_config.get_model(model_name)
    instances = model.objects.all()

    context = {
        'model_name': model_name,
        'instances': instances,
    }

    return render(request, "myApp/admin_panel_detail.html", context)


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='home')  # Redirect to 'home' if not an admin
def admin_panel_detail_instance(request, model_name, instance_id):
    app_config = apps.get_app_config('myApp')
    model = app_config.get_model(model_name)
    instance = get_object_or_404(model, id=instance_id)

    # Generate a ModelForm dynamically
    ModelForm = modelform_factory(model, exclude=['id'])

    if request.method == 'POST':
        form = ModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/admin_panel/{model_name}/')  # Redirect to the list of instances
    else:
        form = ModelForm(instance=instance)

    context = {
        'model_name': model_name,
        'instance': instance,
        'form': form,
    }

    return render(request, "myApp/admin_panel_detail_instance.html", context)


@login_required
def admin_panel_save_instance(request, model_name, instance_id):
    app_config = apps.get_app_config('myApp')
    model = app_config.get_model(model_name)
    instance = get_object_or_404(model, id=instance_id)

    ModelForm = get_dynamic_model_form(model)

    if request.method == 'POST':
        form = ModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/admin_panel/{model_name}/')  # Redirect to the list of instances
    else:
        form = ModelForm(instance=instance)

    context = {
        'model_name': model_name,
        'instance': instance,
        'form': form,
    }

    return render(request, "myApp/admin_panel_detail_instance.html", context)

@login_required
def location(request):
    locations = Location.objects.all()  

  
    for location in locations:
        if location.crime_percentage > 50:
            location.status = 'Unsafe'
        else:
            location.status = 'Safe'
        location.save()  

    context = {'locations': locations}
    return render(request, "myApp/location.html", context)

@login_required
def serviceprofile(request, service_id):
    service = get_object_or_404(EmergencyService, pk=service_id)
    context = {'service': service}
    return render(request, "myApp/serviceprofile.html", context)

@login_required
def emergency(request):
    emergency_services = EmergencyService.objects.all()
    context = {'emergency_services': emergency_services}
    return render(request, "myApp/emergency.html", context)

@login_required
def criminalprofile(request, criminal_id):
    criminal = get_object_or_404(Criminal, pk=criminal_id)
    context = {'criminal': criminal}
    return render(request, "myApp/criminalprofile.html", context)

@login_required
def criminal(request):
    criminals = Criminal.objects.all()
    context = {'criminals': criminals}
    return render(request, "myApp/criminal.html", context)

@login_required
def report(request):
    if request.method == 'POST':
        description = request.POST.get('message')
        timestamp = request.POST.get('Time-Stamp')

        # Ensure the timestamp is not in the future
        current_datetime = timezone.now()
        report_datetime = timezone.make_aware(timezone.datetime.fromisoformat(timestamp), timezone.get_current_timezone())

        if report_datetime > current_datetime:
            return HttpResponse('Timestamp cannot be in the future')

        area_code = request.POST.get('Area Code')
        crime_type_name = request.POST.get('Crime Type')
        anonymity_status = request.POST.get('Anonymity Status') == 'on'

        try:
            location = Location.objects.get(area_code=area_code)
        except Location.DoesNotExist:
            return HttpResponse('Invalid Area Code')


        try:
            crime_type = CrimeType.objects.get(name=crime_type_name)
        except CrimeType.DoesNotExist:
            return HttpResponse('Invalid Crime Type')

        incident = IncidentReport(
            description=description,
            timestamp=timestamp,
            anonymity_status=anonymity_status,
            location=location,
            crime_type=crime_type
        )
        incident.save()

        # Create a related notification for the incident
        notification = Notification(
            incident_report=incident,
            crime_type=crime_type,
            alert_message=description  # You can use the description as the alert message
        )
        notification.save()

        # Check if the reported crime type is "Missing Person" or "Prisoner Escape"
        if crime_type_name == "Missing Person" or crime_type_name == "Prisoner Escape":
            # Send notifications to all users of the specific location
            users_to_notify = User.objects.filter(userprofile__location=location)
            for user in users_to_notify:
                user_profile = user.userprofile
                user_profile.notifications.add(notification)

        update_location_crime_percentage(location)

        # Update crime percentage for all locations
        locations = Location.objects.all()
        for location in locations:
            update_location_crime_percentage(location) 
        return render(request, "myApp/home.html")

    locations = Location.objects.all()
    crime_types = CrimeType.objects.all()

    context = {
        'locations': locations,
        'crime_types': crime_types,
    }

    return render(request, "myApp/report.html", context)


def update_location_crime_percentage(location):
    total_reports = IncidentReport.objects.filter(location=location).count()

    if total_reports > 0:
        crime_percentage = (total_reports / IncidentReport.objects.count()) * 100

        location.crime_percentage = crime_percentage
        location.save()
    else:
        location.crime_percentage = 0
        location.save()

@csrf_exempt
def send_location(request):
    if request.method == 'POST':
        data = request.POST
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        location_details = get_location_details(latitude, longitude)

        send_email_with_location(location_details)

        return JsonResponse({'message': 'Location sent successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def get_location_details(latitude, longitude):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.reverse((latitude, longitude), language='en')
    
    address = location.address if location else 'Unknown Address'
    return address


# def report(request):
#     # existing code for creating a report and notification...
#     user_profile = request.user.userprofile
#     notifications_count = user_profile.notifications.count()
#     request.session['notifications_count'] = notifications_count  # update session
#     return HttpResponse('Incident Report saved successfully')


@login_required
def notification(request):
    user = request.user
    user_profile = user.userprofile

    # Reset the session notification count
    request.session['notifications_count'] = 0
    request.session['reset_notifications'] = True
    request.session.modified = True

    notifications = user_profile.notifications.all().order_by('-timestamp')

    # Optional: Mark notifications as read
    for notification in notifications:
        notification.is_read = True
        notification.save()

    context = {'notifications': notifications}
    return render(request, "myApp/notification.html", context)



def send_email_with_location(location_details):
    sender_email = 'mahiyatasnim200021@gmail.com'  # Replace with your email
    sender_password = 'kxze ylnq rjtn vsdj'  # Replace with your App Password
    receiver_email = '21101069@uap-bd.edu'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Send Help in This Location'

    body = f'Location Details:\n{location_details}'
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)


def ml_results(request):
    data = pd.read_csv('/workspaces/SwiftAlert/myProject/myApp/crime_data_bangladesh.csv')

    data['overall_crime_rate'] = data.drop(['area_name', 'year'], axis=1).sum(axis=1)

    X = data.drop(['area_name', 'year', 'overall_crime_rate'], axis=1)
    y = data['overall_crime_rate']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_regressor.fit(X_train, y_train)

    y_train_pred = rf_regressor.predict(X_train)

    mae_train = mean_absolute_error(y_train, y_train_pred)
    mse_train = mean_squared_error(y_train, y_train_pred)
    rmse_train = mean_squared_error(y_train, y_train_pred, squared=False)
    r2_train = r2_score(y_train, y_train_pred)

    y_test_pred = rf_regressor.predict(X_test)

    mae_test = mean_absolute_error(y_test, y_test_pred)
    mse_test = mean_squared_error(y_test, y_test_pred)
    rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)
    r2_test = r2_score(y_test, y_test_pred)

    # Creating plots
    plt.figure(figsize=(12, 6))

    # Training set scatter plot
    plt.subplot(1, 2, 1)
    plt.scatter(y_train, y_train_pred, color='blue', alpha=0.5, label='Actual vs. Predicted')
    plt.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], color='red', linestyle='--', label='Perfect Prediction')
    plt.xlabel('Actual Overall Crime Rate')
    plt.ylabel('Predicted Overall Crime Rate')
    plt.title('Training Set - Actual vs. Predicted')
    plt.legend()

    # Test set scatter plot
    plt.subplot(1, 2, 2)
    plt.scatter(y_test, y_test_pred, color='green', alpha=0.5, label='Actual vs. Predicted')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Perfect Prediction')
    plt.xlabel('Actual Overall Crime Rate')
    plt.ylabel('Predicted Overall Crime Rate')
    plt.title('Test Set - Actual vs. Predicted')
    plt.legend()

    # Save the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convert the plot to base64 for HTML rendering
    graph = base64.b64encode(image_png).decode('utf-8')

    # Pass data to template
    context = {
        'mae_train': mae_train,
        'mse_train': mse_train,
        'rmse_train': rmse_train,
        'r2_train': r2_train,
        'mae_test': mae_test,
        'mse_test': mse_test,
        'rmse_test': rmse_test,
        'r2_test': r2_test,
        'graph': graph,
    }

    return render(request, 'myApp/ml_results.html', context)

def crime_analysis(request):
    data = pd.read_csv('/workspaces/SwiftAlert/myProject/myApp/crime_data_bangladesh.csv')

    # Initialize lists to store results for all areas
    area_results = []

    for area_name, area_data in data.groupby('area_name'):
        area_result = {}

        area_data['overall_crime_rate'] = area_data.drop(['area_name', 'year'], axis=1).sum(axis=1)

        X = area_data.drop(['area_name', 'year', 'overall_crime_rate'], axis=1)
        y = area_data['overall_crime_rate']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_regressor.fit(X_train, y_train)

        y_test_pred = rf_regressor.predict(X_test)

        rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)

        # Determine safety status based on test RMSE
        safety_status = 'Safe' if rmse_test < 2000 else 'Unsafe'

        # Populate area result dictionary
        area_result['area_name'] = area_name
        area_result['test_rmse'] = rmse_test
        area_result['safety_status'] = safety_status

        # Append area result to list
        area_results.append(area_result)

    context = {
        'area_results': area_results,
    }

    return render(request, 'myApp/crime_analysis.html', context)