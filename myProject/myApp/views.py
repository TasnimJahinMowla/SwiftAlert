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
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        myuser=authenticate(username=username, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success (request, "Login Successful")
            return redirect('http://127.0.0.1:8000/home/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('http://127.0.0.1:8000/loginpage/')
    context={}
    return render(request, "myApp/loginpage.html",context)
    

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


def navigation_bar(request):
    context={}
    return render(request, "myApp/navigation_bar.html")
    

def about(request):
    context={}
    return render(request, "myApp/about.html")


def services(request):
    context={}
    return render(request, "myApp/services.html")


def contact(request):
    context={}
    return render(request, "myApp/contact.html")


def notification(request):
    user = request.user
    user_profile = user.userprofile  # Assuming you have a user profile associated with each user

    # Filter notifications for the logged-in user, ordered by timestamp (latest first)
    notifications = user_profile.notifications.all().order_by('-timestamp')

    context = {'notifications': notifications}
    return render(request, "myApp/notification.html", context)

def home(request):
    context={}
    return render(request, "myApp/home.html")

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

def serviceprofile(request, service_id):
    service = get_object_or_404(EmergencyService, pk=service_id)
    context = {'service': service}
    return render(request, "myApp/serviceprofile.html", context)


def emergency(request):
    emergency_services = EmergencyService.objects.all()
    context = {'emergency_services': emergency_services}
    return render(request, "myApp/emergency.html", context)

def criminalprofile(request, criminal_id):
    criminal = get_object_or_404(Criminal, pk=criminal_id)
    context = {'criminal': criminal}
    return render(request, "myApp/criminalprofile.html", context)


def criminal(request):
    criminals = Criminal.objects.all()
    context = {'criminals': criminals}
    return render(request, "myApp/criminal.html", context)

def update_location_crime_percentage(location):
    total_reports = IncidentReport.objects.filter(location=location).count()

    if total_reports > 0:
       
        crime_percentage = (total_reports / IncidentReport.objects.count()) * 100

        location.crime_percentage = crime_percentage
        location.save()



def report(request):
    if request.method == 'POST':
        description = request.POST.get('message')
        timestamp = request.POST.get('Time-Stamp')
        area_code = request.POST.get('Area Code')
        crime_type_name = request.POST.get('Crime Type')
        anonymity_status = request.POST.get('Anonymity Status') == 'on'

        try:
            location = Location.objects.get(area_code=area_code)
        except Location.DoesNotExist:
            return JsonResponse({'message': 'Invalid Area Code', 'alert_type': 'danger'})

        try:
            crime_type = CrimeType.objects.get(name=crime_type_name)
        except CrimeType.DoesNotExist:
            return JsonResponse({'message': 'Invalid Crime Type', 'alert_type': 'danger'})

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
            alert_message=description,  # You can use the description as the alert message
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

        locations = Location.objects.all()
        for location in locations:
            update_location_crime_percentage(location)

        return JsonResponse({'message': 'Incident Report saved successfully', 'alert_type': 'success'})

        locations = Location.objects.all()
        for location in locations:
            update_location_crime_percentage(location)

        return JsonResponse({'message': 'Incident Report saved successfully', 'alert_type': 'success'})

    
    locations = Location.objects.all()
    crime_types = CrimeType.objects.all()

    context = {
        'locations': locations,
        'crime_types': crime_types,
    }

    return render(request, "myApp/report.html", context)



def mark_notification_as_read(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notificationId')
        try:
            notification = Notification.objects.get(pk=notification_id)
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error'})

def update_location_crime_percentage(location):
    total_reports = IncidentReport.objects.filter(location=location).count()

    if total_reports > 0:
        
        crime_percentage = (total_reports / IncidentReport.objects.count()) * 100

        
        location.crime_percentage = crime_percentage
        location.save()
    else:
        
        location.crime_percentage = 0
        location.save()

